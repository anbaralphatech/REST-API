import requests, logging
from flask_restful import fields
from flask import Blueprint
from blueprints import db
from flask_restful import Api, Resource, reqparse, marshal
# ===== Untuk import __init__.py =====
from . import *

bp_loc = Blueprint('locs', __name__)
api = Api(bp_loc)

class PublicGetCurrentLoc(Resource):
    wio_host = "http://dev.farizdotid.com/api/instansi/semuainstansi"
    
    # @jwt_required
    def get(self):
        rq = requests.get(self.wio_host)
        current = rq.json()
        list_loc = []
        for i in current['instansi']:
            tabelling = Locs(None, i['nama_kabupaten'] ,i['jenis_instansi'], i['nama_instansi'], i['alamat_instansi'])
            db.session.add(tabelling)
            db.session.commit()
            marshal_data = marshal(tabelling, Locs.response_field)
            list_loc.append(marshal_data)
        return list_loc


api.add_resource(PublicGetCurrentLoc, '')