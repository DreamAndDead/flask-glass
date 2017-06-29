from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config

db = SQLAlchemy()


def create_app(config_name):
    """ development, test or production """
    app = Flask(__name__)
    CORS(app)
    Migrate(app, db)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    from .route import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
