from routes.__init__ import make_response, Resource, jwt_required, current_user
from models.transaction import Transaction
from models.expense import Expense


class TransactionsGet(Resource):
    @jwt_required()
    def get(self):
        try:
            expenses = Expense.query.filter_by(id=current_user.id).all()
            if not expenses:
                return make_response({"message": "No expesnes found for this user."}, 404)
            transactions = Transaction.query.filter(Transaction.expense_id.in_([expense.id for expense in expenses])).all()
            return make_response([transaction.to_dict() for transaction in transactions], 200)
        except Exception as e:
            return make_response({"error": str(e)}, 500)
