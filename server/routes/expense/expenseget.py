from routes.__init__ import make_response, Resource, jwt_required
from models.expense import Expense
from models.budget import Budget
from flask_jwt_extended import current_user


class ExpensesGet(Resource):
    @jwt_required()
    def get(self):
        try:
            budgets = Budget.query.filter_by(user_id=current_user.id).all()
            if not budgets:
                return make_response({"message": "No budgets found for the user."}, 404)
            expenses = Expense.query.filter(Expense.budget_id.in_([budget.id for budget in budgets])).all()
            if not expenses:
                return make_response({"message": "No expenses found."}, 404)
            return make_response([expense.to_dict() for expense in expenses], 200)
        except Exception as e:
            return make_response({"error": str(e)}, 500)