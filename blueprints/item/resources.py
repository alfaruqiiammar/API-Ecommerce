import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from . import *
import random
from sqlalchemy import desc
from .models import Items
from flask_jwt_extended import jwt_required

from blueprints import db, app, internal_required


bp_item = Blueprint('item', __name__)
api = Api(bp_item)


class ItemResource(Resource):

    def __init__(self):
        pass

    def options(self):
        return {"Success": "Ok"}, 200

    # @jwt_required
    # @internal_required
    def delete(self, item_id=11):
        qry = Items.query.get(item_id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        db.session.delete(qry)
        db.session.commit()

        return {'status': 'DELETED'}, 200

    # @jwt_required
    # @internal_required

    def get(self, item_id=None):
        qry = Items.query.get(item_id)
        if qry is not None:
            return marshal(qry, Items.response_fields), 200
        return {'status': 'NOT_FOUND'}, 404

    # @jwt_required
    # @internal_required

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nama', location='json', required=True)
        parser.add_argument('detail', location='json', required=True)
        parser.add_argument('url', location='json', required=True)
        parser.add_argument('harga', location='json', required=True)
        parser.add_argument('total', location='json', required=True)
        args = parser.parse_args()

        item = Items(args['nama'], args['detail'],
                     args['url'], args['harga'],   args['total'])
        db.session.add(item)
        db.session.commit()

        app.logger.debug('DEBUG: %s', item)

        return marshal(item, Items.response_fields), 200

    # @jwt_required
    # @internal_required
    def put(self, item_id=None):
        parser = reqparse.RequestParser()
        # parser.add_argument('item_id', location='json', required=True)
        parser.add_argument('nama', location='json', required=True)
        parser.add_argument('harga', location='json', required=True)
        parser.add_argument('detail', location='json', required=True)
        parser.add_argument('url', location='json', required=True)
        parser.add_argument('total', location='json', required=True)
        args = parser.parse_args()

        qry = Items.query.get(item_id)
        if qry is None:
            return {'status': "NOT_FOUND"}, 404

        # qry.item_id = args['item_id']
        qry.nama = args['nama']
        qry.harga = args['harga']
        qry.detail = args['detail']
        qry.url = args['url']
        qry.total = args['total']

        return marshal(qry, Items.response_fields), 200


class ItemList(Resource):

    def __init__(self):
        pass

    def options(self):
        return {"Success": "Ok"}, 200

    # @jwt_required
    # @internal_required

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', default=1, location='args', type=int)
        parser.add_argument('rp', default=25, location='args', type=int)
        # parser.add_argument('item_id', location='args', help='invalid status')
        # parser.add_argument('nama', location='args', help='invalid status')
        # parser.add_argument('orderby', location='args', help='invalid status', choices=('harga'))
        # parser.add_argument('sort', location='args', help='invalid sort value', choices=('desc', 'asc'))
        args = parser.parse_args()

        offset = (args['p'] * args['rp'] - args['rp'])

        qry = Items.query

        # if args['item_id'] is not None:
        #     qry = qry.filter_by(item_id=args['item_id'])

        # if args['nama'] is not None:
        #     qry = qry.filter_by(nama=args['nama'])

        # if args['orderby'] is not None:
        #     if args['orderby'] == 'harga':
        #         if args['sort'] == 'desc':
        #             qry = qry.order_by(desc(Items.harga))
        #         else:
        #             qry = qry.order_by(Items.harga)
        # if args['orderby'] == 'writer':
        #     if args['sort'] == 'desc':
        #         qry = qry.order_by(desc(Books.writer))
        #     else:
        #         qry = qry.order_by(Books.writer)

        rows = []

        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Items.response_fields))

        return rows, 200


api.add_resource(ItemList, '', '/list')
api.add_resource(ItemResource, '', '/<item_id>')
