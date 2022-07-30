from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'a0adfe916935234964b92d6dae600387' #token generated from secrets library
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////usr/src/app/geo_app/geo.db'
db = SQLAlchemy(app)

from geo_app import routes, models

