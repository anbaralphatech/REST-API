from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal
from . import *
from blueprints import db
import logging, json
from blueprints.client import Client_input
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
# create token
# dapat identity
# middleware dibuat si Flask, pake @ didepannya
# untuk payload

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)

class CreateTokenResources(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location='json', required=True)
        parser.add_argument('client_secret', location='json', required=True)
        args = parser.parse_args()

        # if args['client_key'] == 'abc101' and args['client_secret'] == 'def101':
        #     token = create_access_token(args)
        #     return {'token' : token}, 200
        # else:
        #     return {'status':'UNAUTORIZED', 'message':'invalid key or secret'},401

        qry = Client_input.query.filter_by(client_key=args['client_key']).filter_by(client_secret=args['client_secret']).first()

        if qry is not None:
            token = create_access_token(identity=marshal(qry, Client_input.response_field))
            return {'token' : token}, 200
        else:
            return {'status':'UNAUTORIZED', 'message':'invalid key or secret'},401


api.add_resource(CreateTokenResources, '/token', '/token/<int:id>')