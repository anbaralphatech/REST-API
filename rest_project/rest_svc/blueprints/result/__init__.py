import random, logging
from blueprints import db
from flask_restful import fields

class Result(db.Model):

    __tablename__ = "result"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100))
    language = db.Column(db.String(100))
    job_id = db.Column(db.Integer)
    job_type = db.Column(db.String(1500))
    location = db.Column(db.String(100))
    institution = db.Column(db.String(100))

    # ===== Respon Field =====
    response_field = {
        'user_id': fields.Integer,
        'username': fields.String,
        'language' : fields.String,
        'job_id' : fields.Integer,
        'job_type' : fields.String,
        'location' : fields.String,
        'institution' : fields.String
    }
    
    def __init__(self, user_id, username, language, job_id, job_type, location, institution):
        self.user_id = user_id
        self.username = username
        self.language = language
        self.job_id = job_id
        self.job_type = job_type
        self.location = location
        self.institution = institution

    def __repr__(self):
        return '<Result %r>' % self.user_id
