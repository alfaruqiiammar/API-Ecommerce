import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from . import *
import random
from sqlalchemy import desc
from .models import Users
from flask_jwt_extended import jwt_required, get_jwt_claims

from blueprints import db, app, internal_required


bp_user = Blueprint('user', __name__)
api = Api(bp_user)


class UserResource(Resource):

    def options(self):
        return{"Success": "Ok"}, 200

    @jwt_required
    # @internal_required
    def get(self, user_id=None):
        claim = get_jwt_claims()
        user_id = claim['id']
        qry = Users.query.get(user_id)
        if qry is not None:
            return marshal(qry, Users.response_fields), 200
        return {'status': 'NOT_FOUND'}, 404

    # @jwt_required
    # @internal_required

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('status', location='json',
                            type=bool, required=True)
        args = parser.parse_args()

        user = Users(args['username'], args['email'],
                     args['password'], args['status'])
        db.session.add(user)
        db.session.commit()

        app.logger.debug('DEBUG: %s', user)

        return marshal(user, Users.response_fields), 200

    @jwt_required
    # @internal_required
    def put(self, user_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('status', location='json',
                            type=bool, required=True)
        args = parser.parse_args()

        qry = Users.query.get(user_id)
        if qry is None:
            return {'status': "NOT_FOUND"}, 404

        qry.username = args['username']
        qry.email = args['email']
        qry.password = args['password']
        qry.status = args['status']

        return marshal(qry, Users.response_fields), 200

    @jwt_required
    # @internal_required
    def delete(self, user_id=None):
        qry = Users.query.get(user_id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        db.session.delete(qry)
        db.session.commit()

        return {'status': 'DELETED'}, 200


class UserList(Resource):
    def options(self):
        return{"ok": "succes"}, 200

    def __init__(self):
        pass

    @jwt_required
    @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', default=1, location='args', type=int)
        parser.add_argument('rp', default=25, location='args', type=int)
        parser.add_argument('status', type=inputs.boolean, location='args',
                            help='invalid status', choices=(True, False))
        parser.add_argument('orderby', location='args',
                            help='invalid status', choices=('username', 'status'))
        parser.add_argument('sort', location='args',
                            help='invalid sort value', choices=('desc', 'asc'))
        args = parser.parse_args()

        offset = (args['p'] * args['rp'] - args['rp'])

        qry = Users.query

        if args['status'] is not None:
            qry = qry.filter_by(status=args['status'])

        # if args['orderby'] is not None:
        #     if args['orderby'] == 'client_key':
        #         if args['sort'] == 'desc':
        #             qry = qry.order_by(desc(Clients.client_key))
        #         else:
        #             qry = qry.order_by(Clients.client_key)
        #     if args['orderby'] == 'status':
        #         if args['sort'] == 'desc':
        #             qry = qry.order_by(desc(Clients.status))
        #         else:
        #             qry = qry.order_by(Clients.status)

        rows = []

        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Users.response_fields))

        return rows, 200


api.add_resource(UserList, '/list')
api.add_resource(UserResource, '', '/<user_id>')
