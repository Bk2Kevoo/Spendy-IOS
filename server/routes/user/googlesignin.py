
from routes.__init__ import (
    Resource,
    request,
    db,
    make_response,
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
    jwt_required,
    current_user,
)
from models.user import User
from sqlalchemy.exc import IntegrityError
from secrets import token_hex

class GoogleAuth(Resource):
    def post(self):
        try:
            data = request.json
            email = data.get("email")
            name = data.get("name")
            if not email or not name:
                return make_response({"error": "Invalid Google data"}, 400)
            email = email.lower()
            user = User.query.filter_by(email=email).first()
            initial_sign_up = None
            if not user:
                try:
                    user = User(email=email, name=name)
                    user.password = token_hex(8)
                    initial_sign_up = True
                    db.session.add(user)
                    db.session.commit() 
                    print(f"New user created: {user.name} ({user.email})")
                except IntegrityError as e:
                    db.session.rollback() 
                    print(f"Integrity error: {e.orig}")
                    return make_response({"error": "Email already exists, please log in instead."}, 422)
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)

            response_data = {
                "message": "Logged in with Google",
                "user": user.to_dict(), 
                "iniitial_sign_up": initial_sign_up
            }
            response = make_response(response_data, 200)
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)

            return response
        except Exception as e:
            db.session.rollback()
            print(f"Unexpected error: {str(e)}")
            return make_response({"error": "An unexpected error occurred"}, 500)


class ChangePassword(Resource):
    @jwt_required
    def post(self):
        data = request.get_json()
        new_password = data.get("new_password")
        if not new_password:
            return make_response({"error": "New password is required"}, 400)
        user = User.query.get(current_user.id)
        if not user:
            return make_response({"error": "User not found"}, 404)
        if user.initial_sign_up:
            user.password = new_password
            user.initial_sign_up = False  
            db.session.commit()
            return make_response({"message": "Password successfully changed"}, 200)
        return make_response({"error": "Password change not allowed at this time."}, 400)
