import random, logging
from blueprints import db
from flask_restful import fields

class Locs(db.Model):

    __tablename__ = "weather"
    loc_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_kabupaten = db.Column(db.String(100))
    jenis_instansi = db.Column(db.String(100))
    nama_instansi = db.Column(db.String(100))
    alamat_instansi = db.Column(db.String(1500))
    

    # ===== Respon Field =====
    response_field = {
        'loc_id': fields.Integer,
        'nama_kabupaten': fields.String,
        'jenis_instansi' : fields.String,
        'nama_instansi' : fields.String,
        'alamat_instansi' : fields.String
    }
    
    def __init__(self, loc_id, nama_kabupaten, jenis_instansi, nama_instansi, alamat_instansi):
        self.loc_id = loc_id
        self.nama_kabupaten = nama_kabupaten
        self.jenis_instansi = jenis_instansi
        self.nama_instansi = nama_instansi
        self.alamat_instansi = alamat_instansi

    def __repr__(self):
        return '<Internal %r>' % self.loc_id
