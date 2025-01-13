from routes.__init__ import make_response, Resource, jwt_required, db, request
from models.budget import Budget
from flask_jwt_extended import current_user

class BudgetPost(Resource):
    @jwt_required()
    def post(self):
        try:
            data = request.get_json()

            # Check if required fields are present
            if "name" not in data or "amount" not in data:
                return make_response({"error": "Name and amount are required."}, 400)

            # Create a new budget instance for the logged-in user
            new_budget = Budget(
                name=data["name"],
                amount=data["amount"],
                user_id=current_user.id
            )

            # Add the new budget to the database and commit the transaction
            db.session.add(new_budget)
            db.session.commit()
            return make_response(new_budget.to_dict(), 201)
        except Exception as e:
            return make_response({"error": str(e)}, 500)