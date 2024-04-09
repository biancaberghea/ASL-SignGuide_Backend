from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from RestAPI.controller.auth import routes
