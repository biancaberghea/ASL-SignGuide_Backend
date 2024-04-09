from functools import wraps

import jwt
from flask import current_app, jsonify
from flask import request

from RestAPI.model.user import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return jsonify({
                "message": "Authentication Token is missing!"
            }), 401
        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({
                "message": "Something went wrong"
            }), 500

        return f(current_user, *args, **kwargs)

    return decorated
