from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    Migrate(app, db)

    from myapp import models

    from myapp.main import main_bp
    app.register_blueprint(main_bp, url_prefix='/')

    from myapp.googoodan import googoodan_bp
    app.register_blueprint(googoodan_bp, url_prefix='/googoodan')

    from myapp.fileserver import fileserver_bp
    app.register_blueprint(fileserver_bp, url_prefix='/fileserver')

    return app
