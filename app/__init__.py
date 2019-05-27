import os
import logging
from flask import Flask
from flask_restplus import Api
from pymongo import MongoClient
from flask_mail import Mail


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
