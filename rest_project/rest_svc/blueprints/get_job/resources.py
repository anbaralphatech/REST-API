from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from . import *
# from database import db
import logging, json
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
                                # get token          identity
# from blueprints.client import *
import requests

bp_getjob = Blueprint('getjob',__name__)
api = Api(bp_getjob)

class GetJob (Resource):
    wio_host = 'https://jobs.github.com/positions.json'

    def search(self,values):
        # take = {'description': values}
        # print(take)
        # for k in take['description']:
            # for v in values[k]:
        bahasa = ""
        if 'CSS' in values:
            bahasa += ' CSS '

        if 'Javascript' in values:
            bahasa +=' Javascript '

        if 'C++' in values:
            bahasa +=' C++ '

        if 'C#' in values:
            bahasa +=' C# '

        if 'HTML' in values:
            bahasa +=' HTML '

        if 'Python' in values:
            bahasa +=' Python '

        if 'Ruby' in values:
            bahasa +=' Ruby '

        if 'Java' in values:
            bahasa +=' Java '

        if 'PHP' in values:
            bahasa +=' PHP '

        return bahasa


    def get (self,id=None):
        if id == None:
            parser = reqparse.RequestParser()
            parser.add_argument('description', location='args', default=None)
            parser.add_argument('page', location='args', default=0)
            args = parser.parse_args()


            list_job=[]

            for i in range(1, 8): 
                rq = requests.get(self.wio_host , params={'description': args['description'],'page': i})
                job = rq.json()

                for data in job:
                    description=self.search(data["description"])
                    # print(description)
                    
                    ambil = Getjob(None,data['type'],data['location'],description, data['company_url'])
                    db.session.add(ambil)
                    db.session.commit()
                    get = marshal(ambil, Getjob.response_field)                    
                    list_job.append(get)
            return list_job

        else:
            qry = Getjob.query.get(id)
            if qry is not None:
                # unnecessary response field dapat disolve dengan menggunakan marshal (flask-restful)
                return marshal(qry, Getjob.response_field), 200, {'Content-Type':'application/json'}
            return {'status' : 'NOT_FOUND'}, 404, {'Content-Type':'application/json'}
           
            

         
api.add_resource(GetJob,'','/<int:id>')
