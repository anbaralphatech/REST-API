from flask_restful import fields
import random, logging
from blueprint_challenge import db

class Getjob(db.Model):

    __tablename__ = 'getjob'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    tipe = db.Column(db.String(100))
    lokasi = db.Column(db.String(100))
    deskripsi = db.Column(db.String(100))
    lamar = db.Column(db.String(255))
    
    response_field ={     #pengganti serialize
        'id' : fields.Integer,
        'tipe' : fields.String,
        'lokasi' : fields.String,
        'deskripsi' : fields.String,
        'lamar' : fields.String
    }

    def __init__ (self, id, tipe, lokasi, deskripsi, lamar):
        self.id = id
        self.tipe = tipe
        self.lokasi = lokasi
        self.deskripsi = deskripsi
        self.lamar = lamar
    
    def __repr__(self): 
        return '<getjob %r>' % self.id  #Book itu hanya penamaan,  harus string





            