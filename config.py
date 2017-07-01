"""
different environment have its own configuration. here we get test, development and production

see `manage.py` how to change environment
"""
import os


class BaseConfig:
    """
    configuration that all environment shares

    1. SECRET_KEY
    2. server ip and port
    3. static resource dest dir
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess'
    HOST = '0.0.0.0'
    PORT = 5000
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'files')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    """
    for development

    1. db address
    2. flask DEBUG
    3. sqlalchemy log
    """
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost/development"


class TestConfig(BaseConfig):
    """
    for test

    1. db address
    2. flask DEBUG and TEST
    3. sqlalchemy log
    """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost/testdb"


class ProductionConfig(BaseConfig):
    """
    for production

    1. only db address
    2. close flask DEBUG and TEST
    """
    SQLALCHEMY_DATABASE_URI = "mysql://<address online>"


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test': TestConfig,

    'default': DevelopmentConfig
}
