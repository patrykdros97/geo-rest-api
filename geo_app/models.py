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
    publish_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ip = db.Column(db.String(15), nullable=False)
    timezone = db.Column(db.String(50), nullable=True)
    hostname = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(30), nullable=True)
    region = db.Column(db.String(20), nullable=True)
    country = db.Column(db.String(4), nullable=True)
    loc = db.Column(db.String(20), nullable=True)
    org = db.Column(db.String(50), nullable=True)
    postal = db.Column(db.String(6), nullable=True)

    def to_dict(self):
        return {key:value for key, value in self.__dict__.items()}


db.create_all()
