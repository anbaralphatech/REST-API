import requests, logging
from flask_restful import fields
from flask import Blueprint
from blueprints import db
from flask_restful import Api, Resource, reqparse, marshal
# ===== Untuk import __init__.py =====
from . import *
import random
from ..github import *
from ..get_job import *
from ..loc import *

bp_result = Blueprint('bp_result', __name__)
api = Api(bp_result)

class GetResult(Resource):
    
    def get(self,id=None):
        
        jumlahUser = db.session.query(Github_input).count()
        jumlahLoc = db.session.query(Locs).count()
        jumlahJob = db.session.query(Getjob).count()

        ### munddduuuuurrr
        #########################################################################
        parser = reqparse.RequestParser()
        parser.add_argument('language', location='args')
        args = parser.parse_args()

        UserAll = Github_input.query

        LIST_IDX = []
        if args['language'] is not None:
            UserAll = UserAll.filter(Github_input.language.like("%"+args['language']+"%"))
            jumlahUser = UserAll.count()
        else:
            jumlahUser = db.session.query(Github_input).count()
        
        for i in range(jumlahUser):
            USER = marshal(UserAll[i], Github_input.response_field)
            LIST_IDX.append(USER["user_id"])
        #########################################################################

        LISTRES = []
        # ini user ya
        for i in(LIST_IDX):
            qryGit = Github_input.query.get(i)
            GIT = marshal(qryGit, Github_input.response_field)
            # ini job ya
            for j in range(1,jumlahJob):
                random_loc = random.randrange(1, jumlahLoc, 1)
                
                qryJob = Getjob.query.get(j)
                JOB = marshal(qryJob, Getjob.response_field)

                if (GIT['language'] in JOB['deskripsi']) and (GIT['language'] != ''):
                    qryLoc = Locs.query.get(random_loc)
                    LOC = marshal(qryLoc, Locs.response_field)
                    qryRes =  Result.query.get(i)
                    RES = marshal(qryRes, Result.response_field)
                    RES['username'] = GIT['username']
                    RES['language'] = GIT['language']
                    RES['job_id']= JOB['id']
                    RES['job_type'] = JOB['tipe']
                    RES['location'] = LOC['nama_instansi']
                    RES['institution'] = LOC['jenis_instansi']
                    LISTRES.append(RES)
                    resultnya = Result(None, RES['username'], RES['language'], RES['job_id'], RES['job_type'], RES['location'], RES['institution'])
                    db.session.add(resultnya)

        db.session.commit()
        return LISTRES
        
api.add_resource(GetResult, '', '/<int:id>')