import jwt
import uuid
import requests
from datetime import datetime, timedelta

from geo_app import app, db
from .models import Users, GeoInfo
from .decorators import token_required

from flask import jsonify, make_response, request, Response
from werkzeug.security import generate_password_hash, check_password_hash

IP_URL = 'https://ipinfo.io/json?token=b42314e4fb5646'

@app.route('/')
def start_page() -> 'Response':
    return jsonify({'message':'Welcome in GEO RestAPI'})

@app.route('/register', methods=["POST"])
def sign_up_user() -> 'Response':
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Registration complete!'})

@app.route('/login', methods=['POST'])
def log_in_user() -> 'Response':
    auth = request.authorization
    if not auth.username:
        return make_response('Missing username!', '401', {'Authentication': 'Username during logging required'})
    if not auth.password:
        return make_response('Missing password!', '401', {'Authentication': 'Password during login required'})
    if not auth:
        return make_response('I do not know you!', '401', {'Authentication': 'login required'})
    
    user = Users.query.filter_by(name=auth.username).first()

    if user is not None and check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.utcnow() + timedelta(minutes=45)}, app.config['SECRET_KEY'], "HS256")
        return jsonify({'token': token})

    return make_response('I do not know you!', '401', {'Authentication': 'login required'})

@app.route('/users', methods=['GET'])
def get_users() -> 'Response':
    users = Users.query.all()
    result = list(map(lambda user: {'public_id': user.public_id, 'name': user.name, 'admin': user.admin}, users))
    return jsonify({'users': result})

@app.route('/geo', methods=['POST'])
@token_required
def save_geo(current_user: Users) -> 'Response':
    data = request.get_json()
    ip_addres = requests.get(IP_URL).json()
    if ip_addres.get('readme'):
        del ip_addres['readme']
    new_geo_user = GeoInfo(user_id=current_user.id, name=data['name'], **ip_addres)
    db.session.add(new_geo_user)
    db.session.commit()
    return jsonify({'message': 'New user ID added!'})

@app.route('/geo_info', methods=['GET'])
@token_required
def get_geo_info(current_user: Users) -> 'Response':
    return jsonify({'ip': request.environ['HTTP_X_FORWARDED_FOR']})
    # geo_info = GeoInfo.query.filter_by(user_id=current_user.id).first()
    # return jsonify(geo_info.to_dict()) if geo_info is not None else jsonify({'message': 'No info about user geolocation'})

@app.route('/geo_info/<int:geo_id>', methods=['DELETE'])
@token_required
def delete_geo_info(current_user: Users,  geo_id: int) -> 'Response':

    geo_info = GeoInfo.query.filter_by(id=geo_id, user_id=current_user.id).first()
    if geo_info is None:
        return jsonify({'message': 'Such geo info does not exist'})
    
    db.session.delete(geo_info)
    db.session.commit()
    
    return jsonify({'message': 'Geo info deleted'})
