from routes.__init__ import make_response, Resource, jwt_required, request, db
from models.expense import Expense


class ExpensesById(Resource):
    @jwt_required()
    def get(self, expense_id):
        try:
            # Query the expense based on the provided expense_id
            expense = Expense.query.filter_by(id=expense_id).first()
            
            if not expense:
                return make_response({"message": "Expense not found or you do not have access to this."}, 404)
            
            # Return the expense as a dictionary using the to_dict method
            return make_response(expense.to_dict(), 200)
        
        except Exception as e:
            return make_response({"error": str(e)}, 500)