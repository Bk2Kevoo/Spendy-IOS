from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from os import environ
from datetime import timedelta

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///spendy.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["SESSION_TYPE"] = "sqlalchemy"

# flask-jwt-extended configuration
app.config["JWT_SECRET_KEY"] = environ.get("JWT_SECRET_KEY")
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_CSRF_PROTECTION"] = True
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

# import ipdb; ipdb.set_trace()

jwt = JWTManager(app)
db = SQLAlchemy(app)
app.config["SESSION_SQLALCHEMY"] = db
migrate = Migrate(app, db)
api = Api(app, prefix="/api/v1")
flask_bcrypt = Bcrypt(app)