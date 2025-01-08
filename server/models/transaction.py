from models.__init__ import validates, db, SerializerMixin
from sqlalchemy import Enum
from decimal import Decimal
from datetime import date
from expense import Expense

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
        if not isinstance(amount, (Decimal, float, int)):
            raise TypeError("Amount must be a number")
        if amount <= 0:
            raise ValueError("Amount must be positive")

        # Handle transaction logic for debit and credit
        if self.transaction_type == 'debit':
            # Ensure that debit does not exceed available balance in the expense
            available_balance = self.expense.amount - sum(
                t.amount for t in self.expense.transactions if t.transaction_type == 'debit'
            )
            if amount > available_balance:
                raise ValueError("Debit amount exceeds available balance in the expense.")
        elif self.transaction_type == 'credit':
            # Ensure credit does not exceed the allocated budget of the expense
            if amount > self.expense.amount:
                raise ValueError("Credit amount cannot exceed the allocated budget of the expense.")
        
        return amount

    @validates("date")
    def validates_date(self, _, date):
        if not isinstance(date, date):
            raise TypeError("Date must be a valid date object")
        if date > date.today():
            raise ValueError("Transaction date cannot be in the future.")
        return date

    @validates("expense_id")
    def validates_expense_id(self, _, expense_id):
        # Ensure that the expense_id exists in the database
        expense = Expense.query.get(expense_id)
        if not expense:
            raise ValueError(f"Expense ID {expense_id} does not exist.")
        return expense_id
