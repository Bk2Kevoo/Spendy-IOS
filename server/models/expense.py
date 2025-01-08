from models.__init__ import db, SerializerMixin, validates
from datetime import datetime
from datetime import date
from datetime import timedelta
from decimal import Decimal


class Expense(db.Model, SerializerMixin):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=True)
    amount = db.Column(db.Numeric(10, 2), default=Decimal('0.00'))
    date = db.Column(db.Date)
    created_at = db.Column(db.DateTime,  server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    budget_id = db.Column(db.Integer, db.ForeignKey("budgets.id"))

    def __repr__(self):
        return f"""
            <Expense #{self.id},
                Description: {self.description},
                Amount: {self.amount},
                Date: {self.date},
                Created At: {self.created_at},
                Updated At: {self.updated_at},
                Budget ID: {self.budget_id}>
        """
    
    # Relationships
    budget = db.relationship("Budget", back_populates="expenses", cascade="all, delete-orphan")
    transactions = db.relationship("Transaction", back_populates="expense", cascade="all, delete-orphan")
    
    # Serialize
    serialize_rules = ("-budget.expenses","-transactions.expense",)  


    @validates("description")
    def validates_description(self, _, description):
        if not isinstance(description, str):
            raise TypeError("Description must be a string")
        if len(description) < 3:
            raise ValueError("Description must be at least 3 characters long")
        return description

    
    @validates("amount")
    def validates_amount(self, _, amount):
        if not isinstance(amount, (float, Decimal)):
            raise TypeError("Amount must be a number")
        if amount < 0:
            raise ValueError("Amount must be positive")
        return amount
    
    @validates("date")
    def validates_date(self, _, date):
        if not isinstance(date, date):
            raise TypeError("Date must be a valid date object.")
        grace_period = datetime.today().date() - timedelta(days=30)
        if date > datetime.today().date():
            raise ValueError("Date cannot be in the future.")
        if date < grace_period:
            raise ValueError("Date cannot be more than 30 days in the past.")
        return date
    
    @validates("budget_id")
    def validate_budget(self, _, budget):
        if not isinstance(budget, int):
            raise TypeError("Budget Id must be a integer") 
        return budget
