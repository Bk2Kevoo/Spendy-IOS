from routes.__init__ import make_response, Resource, jwt_required, db
from models.transaction import Transaction

class TransactionDelete(Resource):
    @jwt_required()
    def delete(self, transaction_id):
        try:
            # Find the transaction by ID
            transaction = Transaction.query.filter_by(id=transaction_id).first()

            if not transaction:
                return make_response({"message": "Transaction not found."}, 404)

            # Delete the transaction
            db.session.delete(transaction)
            db.session.commit()

            return make_response({"message": "Transaction deleted successfully."}, 200)

        except Exception as e:
            return make_response({"error": str(e)}, 500)
