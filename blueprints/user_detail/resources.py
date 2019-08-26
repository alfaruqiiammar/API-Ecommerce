import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from . import *
import random
from sqlalchemy import desc
from .models import User_details
from  flask_jwt_extended import jwt_required
from blueprints import db, app, internal_required


bp_user_detail = Blueprint('user_details', __name__)
api = Api (bp_user_detail)

class UserDetailResource(Resource):

    def __init__(self):
        pass

    # @jwt_required
    # @internal_req    # @internal_requiredired
    def get(self, user_details_id=None):
        qry = Users.query.get(user_id)
        if qry is not None:
            return marshal(qry, Users.response_fields), 200
        return {'status': 'NOT_FOUND'}, 404


    # @jwt_required
    # @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nama', location='json', required=True)
        parser.add_argument('alamat', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('nomor_hp', location='json', required=True)
        parser.add_argument('user_id', location='json', required=True)
        args = parser.parse_args()

        user_detail = Users(args['nama'], args['alamat'], args['email'], args['nomor_hp'], args['user_id'])
        db.session.add(user_details)
        db.session.commit()

        app.logger.debug('DEBUG: %s', user_details)

        return marshal(user_details, User_details.response_fields), 200


    # @jwt_required
    # @internal_required
    def put(self, user_details_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('nama', location='json', required=True)
        parser.add_argument('alamat', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('nomor_hp', location='json', required=True)
        parser.add_argument('user_id', location='json', required=True)        
        args = parser.parse_args()

        qry = Users.query.get(user_id)
        if qry is None:
            return {'status': "NOT_FOUND"}, 404

        qry.user_details_id = args['user_details_id']
        qry.nama = args['nama']
        qry.alamat = args['alamat']
        qry.email = args['email']
        qry.nomor_hp = args['nomor_hp']
        qry.user_id = args['user_id']


        return marshal(qry, User_details.response_fields), 200


    # @jwt_required
    # @internal_required
    def delete(self, user_details_id=None):
        qry = Users.query.get(user_details_id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        db.session.delete(qry)
        db.session.commit()

        return {'status': 'DELETED'}, 200


class UserDetailList(Resource):

    def __init__(self):
        pass

    # @jwt_required
    # @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', default=1, location='args', type=int)
        parser.add_argument('rp', default=25, location='args', type=int)
        # parser.add_argument('age', location='args', help='invalid status', choices=(True, False))
        # parser.add_argument('orderby', location='args', help='invalid status', choices=('age', 'sex'))
        # parser.add_argument('sort', location='args', help='invalid sort value', choices=('desc', 'asc'))       
        args = parser.parse_args()
        
        offset = (args['p'] * args['rp'] - args['rp'])

        qry = User_details.query

        # if args['status'] is not None:
        #     qry = qry.filter_by(status=args['status'])

        # if args['orderby'] is not None:
        #     if args['orderby'] == 'age':
        #         if args['sort'] == 'desc':
        #             qry = qry.order_by(desc(Users.age))
        #         else:
        #             qry = qry.order_by(Users.age)
        #     if args['orderby'] == 'sex':
        #         if args['sort'] == 'desc':
        #             qry = qry.order_by(desc(Users.sex))
        #         else:
        #             qry = qry.order_by(Users.sex)

        rows = []

        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Users.response_fields))

        return rows, 200
                

api.add_resource(UserDetailList, '', '/list')
api.add_resource(UserDetailResource, '', '/<user_details_id>')