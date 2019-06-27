import os
import logging
from flask import Flask
from flask_restplus import Api
from pymongo import MongoClient
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from redis import StrictRedis

#Create Flask App Object
application = Flask(__name__)

# Load configuration from config object which defaults to Development
application.config.from_object(os.getenv('FLASK_ENVIRONMENT', 'config.Development'))

#Create mail Object
mail = Mail(application)

# Create MongoDB connection object using Mongo URI and instantiate DB (todo_inventory)
mongo_conn = MongoClient(application.config['MONGO_URI'])
mongo_db = mongo_conn[application.config['DB_NAME']]

# Create Logger object
FORMAT = '%(asctime)s %(module)s %(funcName)s %(message)s'
logging.basicConfig(filename="app.log",
                    format=FORMAT,
                    filemode='w')
logger = logging.getLogger()

#Create api object for flask restplus
api = Api(application, title='Todo App', description='Todo App', version=1.0)

#JWT extension setup
jwt = JWTManager(application)

#Redis DB object
redis_store = StrictRedis(host=application.config['REDIS_HOST'],
                          port=application.config['REDIS_PORT'],
                          db=application.config['REDIS_DB'],
                          decode_responses=True)

@jwt.token_in_blacklist_loader
def check_if_token_is_revoked(decrypted_token):
    jti = decrypted_token['jti']
    entry = redis_store.get(jti)
    if entry is None:
        return True
    return entry == 'true'

