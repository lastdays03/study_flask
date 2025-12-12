from flask import Blueprint

googoodan_bp = Blueprint('googoodan', __name__)

from . import routes
