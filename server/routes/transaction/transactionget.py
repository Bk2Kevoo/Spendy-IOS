from routes.__init__ import make_response, Resource, jwt_required
from models.transaction import Transaction


class TransactionsGet(Resource):
    @jwt_required()
    def get(self, expense_id):
        try:
            transactions = Transaction.query.filter_by(expense_id=expense_id).all()

            if not transactions:
                return make_response({"message": "No transactions found for this expense."}, 404)

            return make_response(
                {"transactions": [transaction.to_dict() for transaction in transactions]},
                200
            )
        except Exception as e:
            return make_response({"error": str(e)}, 500)
