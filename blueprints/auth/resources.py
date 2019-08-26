from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from ..user.models import Users

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)


class CreateTokenResource(Resource):
    def options(self):
        return{"Success": "Ok"}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()

        # ambil dari database
        user_query = Users.query.filter_by(username=args['username']).filter_by(
            password=args['password']).first()
        user_data = marshal(user_query, Users.jwt_response_field)

        if user_query is not None:
            token = create_access_token(identity=user_data, user_claims={
                                        "id": user_query.user_id})
        # if args['client_key'] == 'altarest' and args['client_secret'] == '10opwAPk3q2D':
        #     token = create_access_token(identity=args['client_key'])
        else:
            return {'status': 'UNAUTHORIZED', 'message': 'invalid key or secret'}, 401

        return {'token': token, "data": user_data}, 200

    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        return claims, 200


class RefreshTokenResource(Resource):

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        token = create_access_token(identity=current_user)
        return {'token': token, 'identity': current_user}, 200


api.add_resource(CreateTokenResource, '')
api.add_resource(RefreshTokenResource, '/refresh')
