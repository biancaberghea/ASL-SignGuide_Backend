import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=['http://localhost:4200'])
app.secret_key = "blackyberghea2002"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://Bianca:blacky@localhost:3306/licenta'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
SECRET_KEY = os.environ.get('SERCRET_KEY') or 'top secret'
app.config['SECRET_KEY'] = SECRET_KEY

jwt = JWTManager(app)
