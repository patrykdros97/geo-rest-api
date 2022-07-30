import jwt
import uuid
import requests
from datetime import datetime, timedelta

from geo_app import app, db
from .models import Users, GeoInfo

from flask import jsonify, redirect, make_response, url_for, flash, request
from werkzeug.security import generate_password_hash,check_password_hash

@app.route('/')
def start_page():
    return 'Welcome in GEO RestAPI'

@app.route('/register', methods=["POST"])
def sign_up_user():
    data = request.get_json()
    return jsonify({'message': data})
    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Registration complete!'})

@app.route('/login', methods=['POST'])
def log_in_user():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('I do not know you!', '401', {'Authentication': 'login required'})
    
    user = Users.query.filter_by(name=auth.username).first()
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.utcnow() + timedelta(minutes=45)}, app.config['SECRET_KEY'], "HS256")
        return jsonify({'token': token})

    return make_response('I do not know you!', '401', {'Authentication': 'login required'})

@app.route('/users', methods=['GET'])
def get_users():
    users = Users.query.all()
    result = list(map(lambda user: {'public_id': user.public_id, 'name': user.name, 'password': user.password, 'admin': user.admin}, users))
    return jsonify({'users': result})
    
