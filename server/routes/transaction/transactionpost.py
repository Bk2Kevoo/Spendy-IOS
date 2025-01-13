from datetime import datetime
from routes.__init__ import make_response, Resource, jwt_required, request, db
from models.transaction import Transaction

class TransactionsPost(Resource):
    @jwt_required()
    def post(self):
        try:
            data = request.get_json()

            # Validate expense_id
            expense_id = data.get("expense_id")
            if not expense_id:
                return make_response({"message": "Expense ID is required."}, 400)

            # Validate transaction_type
            transaction_type = data.get("transaction_type")
            if transaction_type not in ['credit', 'debit']:
                return make_response({"message": "Transaction type must be either 'credit' or 'debit'."}, 400)

            # Validate amount
            amount = data.get("amount")
            if amount is None or amount <= 0:
                return make_response({"message": "Amount must be a positive number."}, 400)

            # Validate date
            date = data.get("date")
            if not date:
                return make_response({"message": "Date is required."}, 400)

            # Ensure the date is in correct format
            try:
                transaction_date = datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                return make_response({"message": "Date must be in YYYY-MM-DD format."}, 400)

            # Create new transaction
            new_transaction = Transaction(
                expense_id=expense_id,
                transaction_type=transaction_type,
                amount=amount,
                date=transaction_date
            )

            # Add to database
            db.session.add(new_transaction)
            db.session.commit()

            return make_response({"message": "Transaction created successfully.", "transaction": new_transaction.to_dict()}, 201)

        except Exception as e:
            return make_response({"error": str(e)}, 500)
