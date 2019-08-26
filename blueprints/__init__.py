
import json
import logging
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from datetime import timedelta
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from functools import wraps
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['APP_DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1:3306/ecommerce'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# JWT
app.config['JWT_SECRET_KEY'] = 'SFsieaaBsLEpecP675r243faM8oSB2hV'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_acces_token(identity):
    return identity


db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


def internal_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if not claims['status']:
            return {'status': 'FORBIDDEN', 'message': 'Internal Only!'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper

# akses eksternal


def external_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['status']:
            return {'status': 'FORBIDDEN', 'message': 'Internal Only!'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper

################################
# Middlewares (log)
###############################


@app.after_request  # -> decorator
def after_request(response):
    # GET dikasih if karena pake param (tidak meneirma input body) jadi tidak bisa langsung get_json dan harus pake args
    try:
        if request.method == 'GET':
            app.logger.warning("REQUEST_LOG\t%s",
                               json.dumps({
                                   'method': request.method,
                                   'code': response.status,
                                   'uri': request.full_path,
                                   'request': request.args.to_dict(),
                                   'response': json.loads(response.data.decode('utf-8'))
                               })
                               )
        else:
            app.logger.warning("REQUEST_LOG\t%s",
                               json.dumps({
                                   'uri': request.full_path,
                                   'request': request.get_json(),
                                   'response': json.loads(response.data.decode('utf-8'))
                               })
                               )
    except Exception as e:
        app.logger.error("REQUEST_LOG\t%s",
                         json.dumps({
                             'uri': request.full_path,
                             'request': {},
                             'response': json.loads(response.data.decode('utf-8'))
                         })
                         )
    return response


# from blueprints.transaksi_detail.resources import bp_transaksi_detail
# from blueprints.cart.resoruces import bp_cart
# from blueprints.user_detail.resources import bp_user_detail
from blueprints.user.resources import bp_user
from blueprints.auth.resources import bp_auth
from blueprints.item.resources import bp_item
from blueprints.transaksi.resources import bp_transaksi
# app.register_blueprint(bp_client, url_prefix='/client')
app.register_blueprint(bp_user, url_prefix='/user')
app.register_blueprint(bp_auth, url_prefix='/auth')
app.register_blueprint(bp_item, url_prefix='/item')
app.register_blueprint(bp_transaksi, url_prefix='/transaksi')
# app.register_blueprint(bp_transaksi_detail, url_prefix='/transaksiDetail')
# app.register_blueprint(bp_cart, url_prefix='/cart')
# app.register_blueprint(bp_user_detail, url_prefix='/user_detail')
# app.register_blueprint(bp_admin, url_prefix='/admin')


db.create_all()
