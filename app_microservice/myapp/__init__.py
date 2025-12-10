from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    # Blueprint 등록
    from myapp.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from myapp.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
