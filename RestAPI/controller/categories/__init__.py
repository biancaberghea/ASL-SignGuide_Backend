from flask import Blueprint

cat_bp = Blueprint('categories', __name__)

from RestAPI.controller.categories import routes