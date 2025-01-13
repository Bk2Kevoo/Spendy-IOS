from routes.__init__ import make_response, Resource, jwt_required, request, db
from datetime import datetime
from models.transaction import Transaction

class TransactionPatch(Resource):
    @jwt_required()
    def patch(self, transaction_id):
        try:
            data = request.get_json()

            # Find the transaction by ID
            transaction = Transaction.query.filter_by(id=transaction_id).first()

            if not transaction:
                return make_response({"message": "Transaction not found."}, 404)

            # Update fields if provided in the request
            if "transaction_type" in data:
                if data["transaction_type"] not in ["credit", "debit"]:
                    return make_response({"message": "Transaction type must be 'credit' or 'debit'."}, 400)
                transaction.transaction_type = data["transaction_type"]

            if "amount" in data:
                if data["amount"] <= 0:
                    return make_response({"message": "Amount must be a positive number."}, 400)
                transaction.amount = data["amount"]

            if "date" in data:
                try:
                    transaction.date = datetime.strptime(data["date"], "%Y-%m-%d").date()
                except ValueError:
                    return make_response({"message": "Date must be in YYYY-MM-DD format."}, 400)

            # Commit changes to the database
            db.session.commit()

            return make_response({"message": "Transaction updated successfully.", "transaction": transaction.to_dict()}, 200)

        except Exception as e:
            return make_response({"error": str(e)}, 500)
