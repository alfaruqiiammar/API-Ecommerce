import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from . import *
import random
from sqlalchemy import desc
from .models import Transactions
from flask_jwt_extended import jwt_required, get_jwt_claims

from blueprints import db, app, internal_required


bp_transaksi = Blueprint('transaksi', __name__)
api = Api(bp_transaksi)


class TransaksiResource(Resource):

    def __init__(self):
        pass

    def options(self):
        return {"Success": "Ok"}, 200

    @jwt_required
    # @internal_required
    def get(self, transaksi_id=None):
        qry = Transactions.query.get(transaksi_id)
        if qry is not None:
            return marshal(qry, Transactions.response_fields), 200
        return {'status': 'NOT_FOUND'}, 404

    @jwt_required
    # @internal_required
    def post(self):
        claim = get_jwt_claims()
        user_id = claim['id']
        parser = reqparse.RequestParser()
        parser.add_argument('item_id', location='json', required=True)
        parser.add_argument('total_qty', location='json', required=True)
        parser.add_argument('total_harga', location='json', required=True)
        args = parser.parse_args()

        transaksi = Transactions(
            user_id, int(args['item_id']), int(args['total_qty']), int(args['total_harga']))
        db.session.add(transaksi)
        db.session.commit()

        app.logger.debug('DEBUG: %s', transaksi)

        return marshal(transaksi, Transactions.response_fields), 200

    @jwt_required
    @internal_required
    def put(self, transaksi_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', location='json', required=True)
        parser.add_argument('item_id', location='json', required=True)
        parser.add_argument('total_qty', location='json', required=True)
        parser.add_argument('total_harga', location='json', required=True)
        args = parser.parse_args()

        qry = Transactions.query.get(transaksi_id)
        if qry is None:
            return {'status': "NOT_FOUND"}, 404

        qry.transaksi_id = args['transaksi_id']
        qry.user_id = args['user_id']
        qry.item_id = args['item_id']
        qry.total_qty = args['total_qty']
        qry.total_harga = args['total_harga']

        return marshal(qry, Transactions.response_fields), 200

    @jwt_required
    @internal_required
    def delete(self, transaksi_id=None):
        qry = Transactions.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        db.session.delete(qry)
        db.session.commit()

        return {'status': 'DELETED'}, 200


class TransaksiList(Resource):

    def __init__(self):
        pass

    def options(self):
        return {"Success": "Ok"}, 200

    @jwt_required
    # @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', default=1, location='args', type=int)
        parser.add_argument('rp', default=25, location='args', type=int)
        parser.add_argument('user_id', location='args', help='invalid status')
        # parser.add_argument('nama', location='args', help='invalid status')
        # parser.add_argument('orderby', location='args', help='invalid status', choices=('harga'))
        # parser.add_argument('sort', location='args', help='invalid sort value', choices=('desc', 'asc'))
        args = parser.parse_args()

        offset = (args['p'] * args['rp'] - args['rp'])

        qry = Transactions.query

        if args['user_id'] is not None:
            qry = qry.filter_by(user_id=args['user_id'])

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
            rows.append(marshal(row, Transactions.response_fields))

        return rows, 200


api.add_resource(TransaksiList, '', '/list')
api.add_resource(TransaksiResource, '', '/<transaksi_id>')
