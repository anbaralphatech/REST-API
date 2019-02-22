from flask import Flask, request
import logging, json
from flask_restful import Api, fields
from time import strftime
from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from blueprints import db

class Client_input(db.Model):
    __tablename__ = 'client'
    client_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_key = db.Column(db.String(50), unique=True)
    client_secret = db.Column(db.String(25), unique=True)
    status = db.Column(db.Boolean(25))

    # Response Field
    response_field = {
        'client_id' : fields.Integer,
        'client_key' : fields.String,
        'client_secret' : fields.String,
        'status' : fields.Boolean
    }

    # inisiasi dengan menggunakan db
    def __init__(self, client_id, client_key, client_secret, status):
        self.client_id = client_id
        self.client_key = client_key
        self.client_secret = client_secret
        self.status = status

    def __repr__(self):
        return '<Client %d>' %self.client_id