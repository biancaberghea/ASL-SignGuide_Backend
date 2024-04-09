from flask import request, jsonify
from flask_login import login_required
from werkzeug.security import generate_password_hash

from RestAPI.controller.auth import auth_bp
from RestAPI.service.auth_service import auth_service


@auth_bp.before_app_first_request
def create_admin():
    auth_service.create_admin()


@auth_bp.route('/loginUser', methods=['POST'])

def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    return auth_service.login(email, password)


@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = generate_password_hash(data.get('password'), method='pbkdf2:sha256')

    return auth_service.sign_up(email, password, username)


@auth_bp.route('/refreshToken')
def refresh_toke():
    token = auth_service.refresh_authentication()
    return jsonify({'access_token': token})


@auth_bp.route('/getUsername', methods=['GET'])
@login_required
def get_username():
    return auth_service.get_username()


@auth_bp.route('/getUserID', methods=['GET'])
@login_required
def get_user_id():
    return auth_service.get_user_id()


@auth_bp.route('/getRole', methods=['GET'])
@login_required
def get_role():
    return auth_service.get_user_role()
