import requests
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal
from . import *
from blueprints import db
import logging, json
from blueprints.client import Client_input
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

bp_github = Blueprint('bp_github', __name__)
api = Api(bp_github)

class GithubLogin(Resource):
    wio_host = 'https://api.github.com'

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('q', location='args')
        parser.add_argument('type', location='args')
        parser.add_argument('page', location='args')
        parser.add_argument('per_page', location='args')
        args = parser.parse_args()

        LIST_USER = []
        # user in indonesia
        rq = requests.get(self.wio_host + '/search/users', params={'q':args['q'],'type':args['type'], 'page':args['page'], 'per_page':args['per_page']})
        layer1 = rq.json()
        itemList = layer1["items"]
        lenght = len(itemList)
        
        # go to user detail
        for j in range(lenght):
            DICT_DATA = {}
            username = itemList[j]["login"]
            DICT_DATA['username'] = username
            rq2 = requests.get(self.wio_host + '/users/%s/repos' %username)
            layer2 = rq2.json()
            lenght2 = len(layer2)
            # find language
            str_Language = ''
            for k in range(lenght2):
                LIST_Language = []
                language = layer2[k]["language"]
                if language is not None:
                    str_Language += language
            
            DICT_DATA['language'] = str_Language
    
            LIST_USER.append(DICT_DATA)

            github = Github_input(None, DICT_DATA['username'], DICT_DATA['language'])
            db.session.add(github)

        db.session.commit()

        return LIST_USER
    
api.add_resource(GithubLogin, '/search/users')