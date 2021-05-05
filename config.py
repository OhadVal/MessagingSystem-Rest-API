import os


class Config(object):
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_PROD")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER = {'uiversion': 3}

