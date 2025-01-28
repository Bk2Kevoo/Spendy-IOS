from flask_jwt_extended import decode_token
from routes.__init__ import Resource, request, db, flask_bcrypt
from models.user import User
from flask import jsonify

class ResetPassword(Resource):
    def post(self):
        # Get new password and token from request
        data = request.get_json()
        new_password = data.get("new_password")
        reset_token = request.headers.get("Authorization", "").split(" ")[-1]  

        if not reset_token or not new_password:
            return jsonify({"message": "New password and reset token are required"}), 400

        # Validate new_password (example: length check)
        if len(new_password) < 7:
            return jsonify({"message": "Password must be at least 8 characters long"}), 400

        # Decode the token to get the user ID
        try:
            decoded_token = decode_token(reset_token)
            user_id = decoded_token["identity"]
        except Exception as e:
            return jsonify({"message": f"Invalid or expired token: {str(e)}"}), 400

        # Find the user in the database
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        try:
            # Hash the new password
            hashed_password = flask_bcrypt.generate_password_hash(new_password).decode("utf-8")

            # Update the user's password
            user.password = hashed_password
            db.session.commit()

            return jsonify({"message": "Password has been successfully reset"}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"An error occurred while resetting the password: {str(e)}"}), 500
