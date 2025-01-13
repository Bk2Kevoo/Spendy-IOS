from datetime import datetime
from models.expense import Expense
from models.budget import Budget
from routes.__init__ import jwt_required, current_user, db, request, make_response, Resource


class ExpensesPatch(Resource):
    @jwt_required()
    def patch(self, expense_id):  # Accept `expense_id` as a URL parameter
        try:
            # Find the expense by its ID
            expense = Expense.query.filter_by(id=expense_id).first()

            # Check if the expense exists
            if not expense:
                return make_response({"error": "Expense not found."}, 404)

            # Check if the associated budget belongs to the current user
            budget = Budget.query.filter_by(id=expense.budget_id, user_id=current_user.id).first()
            if not budget:
                return make_response({"error": "You are not authorized to update this expense."}, 403)

            # Extract the data from the request body
            data = request.get_json()

            # Update fields based on the request data
            if "amount" in data:
                expense.amount = data["amount"]
            if "description" in data:
                expense.description = data["description"]
            if "date" in data:
                # Convert the date string to a Python date object
                try:
                    expense.date = datetime.strptime(data["date"], "%Y-%m-%d").date()
                except ValueError:
                    return make_response({"error": "Invalid date format. Use YYYY-MM-DD."}, 400)

            # Commit the changes to the database
            db.session.commit()

            # Return the updated expense data as a response
            return make_response(expense.to_dict(), 200)

        except Exception as e:
            return make_response({"error": str(e)}, 500)
