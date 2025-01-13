from models.__init__ import validates, db, SerializerMixin
from sqlalchemy import Enum
from decimal import Decimal
from datetime import date as today_date
from datetime import date
from models.expense import Expense

class Transaction(db.Model, SerializerMixin):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    transaction_type = db.Column(Enum('credit', 'debit', name='transaction_type_enum'))
    amount = db.Column(db.Numeric(10, 2), default=Decimal('0.00')) 
    date = db.Column(db.Date)
    expense_id = db.Column(db.Integer, db.ForeignKey("expenses.id"))

    def __repr__(self):
        return f"""
            <Transaction #{self.id}, 
                Type: {self.transaction_type}, 
                Amount: {self.amount}, 
                Date: {self.date},
                Expense ID: {self.expense_id}>
        """
    
    # Relationships
    expense = db.relationship("Expense", back_populates="transactions")

    # Serialize
    serialize_rules = ("-expense.transactions",)

    # Validations
    @validates("transaction_type")
    def validates_transaction_type(self, _, transaction_type):
        if transaction_type not in ['credit', 'debit']:
            raise ValueError("Transaction type must be either 'credit' or 'debit'")
        return transaction_type

    @validates("amount")
    def validates_amount(self, _, amount):
        if not isinstance(amount, (Decimal, float)):
            raise TypeError("Amount must be a number")
        if amount <= 0:
            raise ValueError("Amount must be positive")

        # # Ensure the 'expense' is properly linked
        # if self.expense is None:
        #     raise ValueError(f"Transaction cannot be processed as Expense ID is invalid.")
        # else:
        #     available_balance = self.expense.amount - sum(
        #         t.amount for t in self.expense.transactions if t.transaction_type == 'debit'
        #     )
        #     if self.transaction_type == 'debit' and amount > available_balance:
        #         raise ValueError("Debit amount exceeds available balance in the expense.")
        #     if self.transaction_type == 'credit' and amount > self.expense.amount:
        #         raise ValueError("Credit amount cannot exceed the allocated budget of the expense.")

        return amount

    @validates("date")
    def validates_date(self, _, transaction_date):
        if not isinstance(transaction_date, date):
            raise TypeError("Date must be a valid date object.")
        
        if transaction_date > today_date.today():  # Use today_date.today() to get current date
            raise ValueError("Date cannot be in the future.")
        
        return transaction_date

    # @validates("expense_id")
    # def validates_expense_id(self, _, expense_id):
    #     if expense_id is None:
    #         raise ValueError("Expense ID cannot be None")
    #     expense = Expense.query.get(expense_id)
    #     if not expense:
    #         raise ValueError(f"Expense ID {expense_id} does not exist.")
    #     return expense_id



