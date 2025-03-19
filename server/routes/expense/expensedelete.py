from routes.__init__ import make_response, Resource, jwt_required, request, db
from models.expense import Expense
from models.budget import Budget
from flask_jwt_extended import current_user

class ExpensesDelete(Resource):
    @jwt_required()
    def delete(self, expense_id):
        try:
            expense = Expense.query.filter_by(id=expense_id).first()

            if not expense:
                return make_response({"error": "Expense not found."}, 404)
            budget = Budget.query.get(expense.budget_id) 
            if budget is None or budget.user_id != current_user.id:
                return make_response({"error": "You are not authorized to delete this expense."}, 403)

            # Delete the expense
            db.session.delete(expense)
            db.session.commit()

            return make_response({"message": "Expense deleted successfully."}, 200)

        except Exception as e:
            return make_response({"error": str(e)}, 500)
