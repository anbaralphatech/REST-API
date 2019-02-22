from flask import Flask, request
import logging, json
from flask_restful import Api, fields
from time import strftime
from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from blueprints import db

class Github_input(db.Model):
    __tablename__ = 'githubuser'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25))
    language = db.Column(db.String(100))

    # Response Field
    response_field = {
        'user_id' : fields.Integer,
        'username' : fields.String,
        'language' : fields.String
    }

    # inisiasi dengan menggunakan db
    def __init__(self, user_id, username, language):
        self.user_id = user_id
        self.username = username
        self.language = language

    def __repr__(self):
        return '<Github %d>' %self.username