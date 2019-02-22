from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort
from time import strftime
import json, logging
from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager
from datetime import timedelta


app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1:3306/rest_training'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

### JWT ###
app.config['JWT_SECRET_KEY'] = '1234'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return identity


db = SQLAlchemy(app)
migrate = Migrate(app,db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# catch 404 default error withh catch_all_404s=True
api = Api(app, catch_all_404s=True)

############
# middleware
############
                                       
@app.after_request
def after_request(response):
    if request.method=="GET":
        app.logger.warning("REQUEST LOG\t\%s %s ", response.status_code, json.dumps({'request':request.args.to_dict(), 'response': json.loads(response.data.decode('utf-8'))}))
    else :  
        app.logger.warning("REQUEST LOG\t\%s %s", response.status_code, json.dumps({'request':request.get_json(), 'response': json.loads(response.data.decode('utf-8'))}))
    return response

# -----CALL BLUEPRINT


from blueprints.get_job.resources import bp_getjob



app.register_blueprint(bp_getjob,url_prefix='/getjob')


db.create_all()