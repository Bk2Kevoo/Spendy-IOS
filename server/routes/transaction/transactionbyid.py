from routes.__init__ import make_response, Resource, jwt_required
from models.transaction import Transaction

class TransactionById(Resource):
    @jwt_required()
    def get(self, transaction_id):
        try:
            transaction = Transaction.query.filter_by(id=transaction_id).first()

            if not transaction:
                return make_response({"message": "Transaction not found."}, 404)

            return make_response({"transaction": transaction.to_dict()}, 200)

        except Exception as e:
            return make_response({"error": str(e)}, 500)
