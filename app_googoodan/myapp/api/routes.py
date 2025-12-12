from flask import jsonify
from . import api_bp
from myapp.models import User

@api_bp.route('/users')
def get_users():
    users = User.query.all()
    return jsonify([{'user_id': user.user_id, 'user_username': user.user_username, 'user_email': user.user_email} for user in users])
