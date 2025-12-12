from flask import Blueprint

fileserver_bp = Blueprint('fileserver', __name__)

from . import routes
