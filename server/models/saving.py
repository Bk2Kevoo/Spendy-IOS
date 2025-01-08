from models.__init__ import db, validates, SerializerMixin
from decimal import Decimal
from datetime import date

class Saving(db.Model, SerializerMixin):
    __tablename__ = "savings"

    # Add Indexes for Performance
    __table_args__ = (
        db.Index('ix_savings_user_id', 'user_id'),
        db.Index('ix_savings_month_year', 'month', 'year'),
    )

    id = db.Column(db.Integer, primary_key=True)
    goal_amount = db.Column(db.Numeric(10, 2), default=Decimal('0.00')) 
    is_completed = db.Column(db.Boolean, default=False)
    month = db.Column(db.Integer, default=date.today().month)
    year = db.Column(db.Integer, default=date.today().year)
    current_savings = db.Column(db.Numeric(10, 2), default=Decimal('0.00')) 
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return f"""
            <Saving #{self.id}, 
                Goal Amount: {self.goal_amount}, 
                Current Savings: {self.current_savings}, 
                Is Completed: {self.is_completed}, 
                Month: {self.month}, 
                Year: {self.year}, 
                User ID: {self.user_id}>
        """

    # Relationships
    user = db.relationship("User", back_populates="savings") 

    # Serialize
    serialize_rules = ("-user.savings",)

    # Validations
    @validates("goal_amount")
    def validates_goal_amount(self, _, goal_amount):
        if not isinstance(goal_amount, (Decimal, float, int)):
            raise TypeError("Goal Amount must be a number")
        if goal_amount < 0:
            raise ValueError("Goal Amount cannot be negative")
        return goal_amount

    @validates("current_savings")
    def validates_current_savings(self, _, current_savings):
        if current_savings > self.goal_amount:
            raise ValueError("Current savings cannot exceed goal amount")
        return current_savings


    @validates("month")
    def validates_month(self, _, month):
        if not isinstance(month, int):
            raise TypeError("Month must be a integer")
        if month < 1 or month > 12:
            raise ValueError("Month must be between 1 and 12")
        return month

    @validates("year")
    def validates_year(self, _, year):
        if not isinstance(year, int):
            raise TypeError("Year must be an integer")
        if year < date.today().year:
            raise ValueError(f"Year must be the current year or a future year.")
        return year
