import os
from datetime import timedelta

class Config(object):
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    SECRET_KEY = os.getenv('SECRET_KEY', 'My-Precious-Key')
    JWT_SECRET_KEY = SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    REDIS_HOST = os.getenv('REDIS_HOST', '0.0.0.0')
    REDIS_PORT = os.getenv('REDIS_HOST', 6379)
    REDIS_DB = os.getenv('REDIS_DB', 0)
    ERROR_INCLUDE_MESSAGE = False

class Development(Config):
    DEBUG = True
    DB_HOST = os.getenv('DB_HOST', '0.0.0.0')
    DB_USER = os.getenv('DB_USER', 'mongoadmin')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
    DB_PORT = os.getenv('DB_PORT', 27017)
    DB_NAME = os.getenv('DB_NAME', 'todo_inventory')
    MONGO_URI = f'''mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}'''
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USER', "development.service@gmail.com")
    MAIL_USERNAME = os.getenv('MAIL_USER', "development.service@gmail.com")
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', "Password@123")
    MAIL_SERVER = os.getenv('MAIL_SERVER', "smtp.gmail.com")
    MAIL_PORT = os.getenv('MAIL_PORT', "587")
    MAIL_USE_TLS = True

class Production(Config):
    DEBUG = False
    DB_HOST = os.getenv('DB_HOST', '0.0.0.0')
    DB_USER = os.getenv('DB_USER', 'productionadmin')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'P@ssw0rd')
    DB_PORT = os.getenv('DB_PORT', 27017)
    DB_NAME = os.getenv('DB_NAME', 'todo_inventory')
    MONGO_URI = f'''mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}'''
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USER', "production.service@gmail.com")
    MAIL_USERNAME = os.getenv('MAIL_USER', "production.service@gmail.com")
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', "P@ssw0rd@123")
    MAIL_SERVER = os.getenv('MAIL_SERVER', "smtp.gmail.com")
    MAIL_PORT = os.getenv('MAIL_PORT', "587")
    MAIL_USE_TLS = True
