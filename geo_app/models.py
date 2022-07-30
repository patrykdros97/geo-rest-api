from geo_app import db
from datetime import datetime

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    password = db.Column(db.String(20))
    admin = db.Column(db.Boolean)

class GeoInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(50))
    addres_ip = db.Column(db.String(15))
    publish_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

db.create_all()
