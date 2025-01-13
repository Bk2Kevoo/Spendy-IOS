from routes.__init__ import make_response, Resource, jwt_required, request, db, current_user
from models.saving import Saving

class SavingsPost(Resource):
    @jwt_required()
    def post(self):
        try:
            data = request.get_json()

            # Validate goal_amount
            goal_amount = data.get("goal_amount")
            if goal_amount is None or goal_amount <= 0:
                return make_response({"message": "Goal amount must be a positive number."}, 400)

            # Validate current_savings
            current_savings = data.get("current_savings")
            if current_savings is None or current_savings < 0:
                return make_response({"message": "Current savings cannot be negative."}, 400)

            # Validate month (1 to 12)
            month = data.get("month")
            if not month or not isinstance(month, int) or not (1 <= month <= 12):
                return make_response({"message": "Month must be an integer between 1 and 12."}, 400)

            # Validate year
            year = data.get("year")
            if not year or not isinstance(year, int) or year < 2000:
                return make_response({"message": "Year must be a valid integer greater than 2000."}, 400)

            # Create a new Saving record
            new_saving = Saving(
                goal_amount=goal_amount,
                current_savings=current_savings,
                is_completed=False,  # Default to False
                month=month,
                year=year,
                user_id=current_user.id
            )

            db.session.add(new_saving)
            db.session.commit()

            # Respond with success
            return make_response({"message": "Saving created successfully.", "saving": new_saving.to_dict()}, 201)

        except Exception as e:
            return make_response({"error": str(e)}, 500)
