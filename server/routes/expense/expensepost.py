from routes.__init__ import make_response, Resource, jwt_required, request, db
from models.expense import Expense
from models.budget import Budget
from flask_jwt_extended import current_user
from datetime import datetime


class ExpensesPost(Resource):
    @jwt_required()
    def post(self):
        try:
            # Get data from the request body
            data = request.get_json()

            # Ensure that required fields are in the data
            if "amount" not in data or "description" not in data or "date" not in data:
                return make_response({"error": "Amount, description, and date are required."}, 400)

            # Convert the date string to a Python date object
            date_obj = datetime.strptime(data["date"], "%Y-%m-%d").date()

            # Get the current user's active budget (for example, first active budget)
            budget = db.session.query(Budget).filter_by(user_id=current_user.id, is_active=True).first()

            if not budget:
                return make_response({"error": "No active budget found."}, 400)

            # Create a new expense instance and associate it with the active budget
            new_expense = Expense(
                amount=data["amount"],
                description=data["description"],
                date=date_obj,  # Store the Python date object
                budget_id=budget.id,  # Automatically assign the active budget ID
            )

            # Add the new expense to the database and commit the transaction
            db.session.add(new_expense)
            db.session.commit()

            # Return the created expense as a response
            return make_response(new_expense.to_dict(), 201)

        except Exception as e:
            return make_response({"error": str(e)}, 500)
