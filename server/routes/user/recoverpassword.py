from flask import request, jsonify
from flask_restful import Resource
from flask_mail import Message
from flask_jwt_extended import create_access_token
from datetime import timedelta
from app import app, db, flask_bcrypt, mail
from models.user import User 


class RequestPasswordReset(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email")
        if not email:
            return jsonify({"message": "Email is required"}), 400


        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"message": "If the email exists, a reset link has been sent"}), 200

        reset_token = create_access_token(
            identity=user.id, 
            additional_claims={"reset": True},  
            expires_delta=timedelta(hours=1)
        )
        frontend_url = app.config.get("FRONTEND_URL", "http://yourfrontend.com") # Fix this once you get your front end URL, RENDER!
        reset_link = f"{frontend_url}/reset-password?token={reset_token}"

        try:
            msg = Message("Password Reset Request", recipients=[email])
            msg.body = f"Click the following link to reset your password:\n\n{reset_link}\n\nIf you did not request this, please ignore this email."
            mail.send(msg)
            return jsonify({"message": "If the email exists, a reset link has been sent"}), 200
        except Exception as e:
            app.logger.error(f"Error sending password reset email: {str(e)}")
            return jsonify({"message": "Failed to send reset email. Please try again later"})
