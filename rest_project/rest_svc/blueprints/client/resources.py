from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal
from . import *
from blueprints import db
from flask_jwt_extended import jwt_required

bp_client = Blueprint('bp_client', __name__)
api = Api(bp_client)

class ClientResource(Resource):

    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location='json', required=True)
        parser.add_argument('client_secret', location='json', required=True)
        parser.add_argument('status', type=bool ,location='json', required=True)
        args = parser.parse_args()

        client = Client_input(None, args['client_key'], args['client_secret'], args['status'])
        db.session.add(client)
        db.session.commit()
        return marshal(client, Client_input.response_field)
        
    @jwt_required
    def get(self, id=None):
        if id == None:
            parser = reqparse.RequestParser()
            parser.add_argument('p', type=int, location='args', default=1)
            parser.add_argument('rp', type=int, location='args', default=5)
            parser.add_argument('client_key', location='args')
            parser.add_argument('client_secret', location='args')
            args = parser.parse_args()

            # kita mau 4 di index ke tiga dengan p=1 rp=5, 4 di index 3
            offset = (args['p'] * args['rp']) - args['rp']
            qry = Client_input.query

            # ini filter gan!
            if args['client_key'] is not None:
                qry = qry.filter_by(client_key=args['client_key'])
                # qry = qry.filter_by(Client_input.client_secret.like("%"+args['client_secret']+"%"))

            LIST = []

            for row in qry.limit(args['rp']).offset(offset).all():
                LIST.append(marshal(row, Client_input.response_field))
            return LIST, 200, {'Content-Type':'application/json'}

        else:
            qry = Client_input.query.get(id)
            if qry is not None:
                # unnecessary response field dapat disolve dengan menggunakan marshal (flask-restful)
                return marshal(qry, Client_input.response_field), 200, {'Content-Type':'application/json'}
            return {'status' : 'NOT_FOUND'}, 404, {'Content-Type':'application/json'}

    @jwt_required
    def put(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location='json', required=True)
        parser.add_argument('client_secret', location='json', required=True)
        parser.add_argument('status', location='json', required=True)
        args = parser.parse_args()

        qry = Client_input.query.get(id)
        qry.client_key = args['client_key']
        qry.client_secret = args['client_secret']
        qry.status = args['status']
                
        db.session.commit()
        return marshal(qry, Client_input.response_field), 200, {'Content-Type':'application/json'}

    @jwt_required
    def delete(self, id=None):
        qry = Client_input.query.get(id)
        if qry is not None:
            db.session.delete(qry)
            db.session.commit()
            return marshal(qry, Client_input.response_field), 200, {'Content-Type':'application/json'}
        return {'status' : 'NOT_FOUND'}, 404, {'Content-Type':'application/json'}


api.add_resource(ClientResource, '/client', '/client/<int:id>')