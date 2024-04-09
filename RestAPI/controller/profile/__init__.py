from flask import Blueprint

profile_bp = Blueprint('profile', __name__)

from RestAPI.controller.profile import routes