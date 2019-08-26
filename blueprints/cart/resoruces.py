import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from . import *
import random
from sqlalchemy import desc
from .models import Cart
from flask_jwt_extended import jwt_required
from ..item.models import Items

from blueprints import db, app, internal_required


bp_cart = Blueprint('cart', __name__)
api = Api (bp_cart)




class CartResource(Resource):

# @jwt_required
    # @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('item_id', location='json', required=True)
        parser.add_argument('user_id', location='json', required=True)
        parser.add_argument('qty', location='json', required=True)
        # parser.add_argument('harga', location='json', required=True)
        args = parser.parse_args()

        data = Items.query.get(int(args['item_id'])).harga * int(args['qty'])

        cart = Cart(args['item_id'], args['user_id'], args['qty'], data)
        db.session.add(cart)
        db.session.commit()

        app.logger.debug('DEBUG: %s', cart)

        return marshal(cart, Cart.response_fields), 200



api.add_resource(CartResource, '', '/<cart_id>')
