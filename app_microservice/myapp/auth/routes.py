from flask import render_template
from . import auth_bp

@auth_bp.route('/login')
def login():
    return "Login Page (Auth Blueprint)"

@auth_bp.route('/register')
def register():
    return "Register Page (Auth Blueprint)"
