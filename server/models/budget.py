from models.__init__ import SerializerMixin, validates, db
from datetime import date
from decimal import Decimal
from sqlalchemy import Enum

class Budget(db.Model, SerializerMixin):
    __tablename__ = "budgets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String )
    total_amount = db.Column(db.Numeric(10, 2), default=Decimal('0.00'), nullable=False)
    start_date= db.Column(db.Date)
    end_date = db.Column(db.Date)
    created_at = db.Column(db.Date, default=date.today)
    updated_at = db.Column(db.Date, default=date.today, onupdate=date.today)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    budget_type = db.Column(Enum('overall', 'monthly', name='budget_type_enum'))


    def __repr__(self):
        return f"""
            <Budget # {self.id}:
                Name: {self.name}
                Description: {self.description}
                Total Amount: {self.total_amount}
                Start Date: {self.start_date}
                End Date: {self.end_date}
                Created At: {self.created_at}
                Updated At: {self.updated_at}
                User ID: {self.user_id}
                Category ID: {self.category_id}
                Budget Type: {self.budget_type}>
        """

    # Relationships
    budget_categories = db.relationship("BudgetCategories", back_populates="budget")
    expenses = db.relationship("Expense", back_populates="budget", cascade="all, delete-orphan")
    user = db.relationship('User', back_populates='budgets')

    # Serialize
    serialize_rules = ("-budget_categories",)

    @validates("name")
    def validates_name(self, _, name):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if len(name) < 3:
            raise ValueError("Name must be 3 characters long")
        return name

    @validates("description")
    def validates_description(self, _, description):
        if not isinstance(description, str):
            raise TypeError("Description must be a string")
        if len(description) < 5:
            raise ValueError("Description must be 4 characters long")
        return description

    @validates("total_amount")
    def valides_total(self, _, total):
        if not isinstance(total, float):
            raise TypeError("Total Amount must be of type Float")
        if total < 0:
            raise ValueError("Total Amount cannot be negative")
        return total


    @validates("start_date")
    def validate_start_date(self, _, start_date):
        # Start date must be a valid date and should be today or in the future
        if not isinstance(start_date, date):
            raise TypeError("Start Date must be a valid date.")
        if start_date < date.today():
            raise ValueError("Start Date must be today or in the future.")
        return start_date

    @validates("end_date")
    def validate_end_date(self, _, end_date):
        # End date must be a valid date and should be later than the start date
        if not isinstance(end_date, date):
            raise TypeError("End Date must be a valid date.")
        if end_date <= self.start_date:
            raise ValueError("End Date must be after Start Date.")
        return end_date

    @validates("user_id")
    def validates_user_id(self, _, user):
        if not isinstance(user, int):
            raise TypeError("User Id must be a integer")
        return user

    @validates("category_id")
    def validates_category_id(self, _, category):
        if not isinstance(category, int):
            raise TypeError("Category Id must be a integer")
        return category

    @validates("budget_type")
    def validate_budget_type(self, _, budget_type):
        allowed_types = ['overall', 'monthly']
        if budget_type not in allowed_types:
            raise ValueError(f"Budget Type must be one of {allowed_types}.")
        return budget_type
