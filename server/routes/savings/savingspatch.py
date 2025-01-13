from routes.__init__ import make_response, Resource, jwt_required, request, db, current_user
from models.saving import Saving
from datetime import datetime

class SavingsPatch(Resource):
    @jwt_required()
    def patch(self, saving_id):
        try:
            data = request.get_json()
            saving = Saving.query.filter_by(id=saving_id, user_id=current_user).first()
            if not saving:
                return make_response({"message": "No Saving found or you do not have access to update this."})
            
            if "goal_amount" in data:
                goal_amount = data.get("goal_amount")
                if goal_amount is None or goal_amount <= 0:
                    return make_response({"message": "Goal amount must be a positive number."}, 400)
                saving.goal_amount = goal_amount

            if "current_savings" in data:
                current_savings = data.get("current_savings")
                if current_savings is None or current_savings < 0:
                    return make_response({"message": "Current savings cannot be negative."}, 400)
                saving.current_savings = current_savings

            if "is_completed" in data:
                is_completed = data.get("is_completed")
                if not isinstance(is_completed, bool):
                    return make_response({"message": "Is_completed must be a boolean value."}, 400)
                saving.is_completed = is_completed

            if "month" in data:
                    # Ensure month is valid (1-12)
                    new_month = int(data.get("month"))
                    if new_month < 1 or new_month > 12:
                        raise ValueError("Month must be between 1 and 12.")
                    saving.month = datetime(datetime.now().year, new_month, 1)
                    
            if "year" in data:
                new_year = data.get("year")
                if not isinstance(new_year, int) or new_year < 2020:  # Example: Ensure a reasonable year range
                    return make_response({"message": "Year must be a valid integer greater than 2020."}, 400)
                saving.year = new_year

            db.session.commit()

            # Return success response
            return make_response({"message": "Saving updated successfully.", "saving": saving.to_dict()}, 200)
            
        except Exception as e:
            return make_response({"error": str(e)}, 500)