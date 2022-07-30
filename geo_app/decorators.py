import jwt
from functools import wraps
from flask import request, jsonify

from geo_app import app
from .models import Users


def token_required(func):

    @wraps(func)
    def decorator(*args, **kwargs):
        token = request.headers['x-access-tokens'] if 'x-access-tokens' in request.headers else None

        if token is None:
            return jsonify({'message': 'A valid token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = Users.query.filter_by(public_id=data('public_id')).first()
        except:
            return jsonify({'message': 'token is valid'})

        return func(current_user, *args, **kwargs)

    return decorator
