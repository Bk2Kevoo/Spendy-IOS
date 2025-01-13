from flask import request, g, render_template, make_response, session
from flask_restful import Resource
from config import db, jwt
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
    unset_access_cookies,
    unset_refresh_cookies,
    unset_jwt_cookies,
    current_user,
    get_jwt
)
from models.user import User
from flask_bcrypt import Bcrypt

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.get(identity)