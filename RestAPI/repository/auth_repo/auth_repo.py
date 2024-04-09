from flask import jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jwt_identity)
from flask_login import current_user, login_user
from sqlalchemy import select, literal, insert
from werkzeug.security import generate_password_hash, check_password_hash

from RestAPI.db.db_init import db
from RestAPI.model.item_table import items
from RestAPI.model.progress_table import user_progress
from RestAPI.model.user import user_datastore, User


def create_admin():
    if not user_datastore.get_user('bergheabianca@icloud.com'):
        password = generate_password_hash('adm1n1strator', method='pbkdf2:sha256')
        admin = User(username='Admin', email='bergheabianca@icloud.com', password=password)
        db.session.add(admin)
        db.session.commit()

        role = user_datastore.find_role('admin')
        user_datastore.add_role_to_user(admin, role)
        user_datastore.commit()


def login(email, password):
    user = user_datastore.get_user(email)

    if user:
        if check_password_hash(user.password.strip(), password):
            login_user(user)
            token = create_access_token(identity=user.username, additional_claims={'role': user.roles[0].name})
            refresh_token = create_refresh_token(identity=user.username, additional_claims={'role': user.roles[0].name})

            return jsonify(
                {'access_token': token, 'refresh_token': refresh_token}), 200
        else:
            return {'message': 'Invalid username or password', 'status': 'error'}, 401
    else:
        return {'message': 'No such user', 'status': 'error'}, 401


def sign_up(email, password, username):
    if user_datastore.get_user(email):
        return {'message': 'User already exists', 'status': 'error'}, 400
    else:
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        # Add the user to the specified role
        role = user_datastore.find_role('user')
        user_datastore.add_role_to_user(new_user, role)
        db.session.commit()

        user = User.query.filter_by(email=email).first()
        create_progress_table(user.id)

        login_user(user)
        token = create_access_token(identity=user.username, additional_claims={'role': user.roles[0].name})
        refresh_token = create_refresh_token(identity=user.username, additional_claims={'role': user.roles[0].name})

        return jsonify(
            {'access_token': token, 'refresh_token': refresh_token}), 200



def create_progress_table(user_id):
    select_query = select(
        literal(user_id).label('user_id'),
        items.c.id.label('word_id'),
        literal(0).label('learned'), literal(0).label('correct_quiz')
    )
    # Executing the insert query
    insert_query = insert(user_progress).from_select(['user_id', 'word_id', 'learned', 'correct_quiz'], select_query)
    db.session.execute(insert_query)
    db.session.commit()


def get_authenticated_user():
    identity = get_jwt_identity()
    return user_datastore.get_user(identity)


def refresh_authentication():
    user = get_authenticated_user()
    return create_access_token(identity=user['email'])


def get_username():
    if current_user.is_authenticated:
        return jsonify({'username': current_user.username})
    else:
        return jsonify({'message': 'User not authenticated'}), 401


def get_user_id():
    if current_user.is_authenticated:
        return jsonify({'id': current_user.id})
    else:
        return jsonify({'message': 'User not authenticated'}), 401


def get_user_role():
    if current_user.is_authenticated:
        if current_user.roles[0].name == 'admin':
            return jsonify({'is_admin': True})
        else:
            return jsonify(({'is_admin': False}))
    else:
        return jsonify({'message': 'Error getting current user'}), 500
