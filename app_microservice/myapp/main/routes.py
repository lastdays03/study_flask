from flask import render_template
from . import main_bp

@main_bp.route('/')
def index():
    return "<h1>Microservice App Index</h1><p><a href='/auth/login'>Login</a> | <a href='/api/users'>API Users</a></p>"
