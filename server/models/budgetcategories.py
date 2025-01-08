from models.__init__ import db, validates, SerializerMixin

class BudgetCategories(db.Model, SerializerMixin):
    __tablename__ = "budgetcategories"

    id = db.Column(db.Integer, primary_key=True)
    budget_id = db.Column(db.Integer, db.ForeignKey("budgets.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    allocated_amount = db.Column(db.Float)

    def __repr__(self):
        return f"""
            <BudgetsCategories #{self.id}
                Budget ID: {self.budget_id}
                Category ID: {self.category_id}
                Allocated Amount: {self.allocated_amount}>
        """
    # Relationships
    budget = db.relationship("Budget", back_populates="budget_categories")
    category = db.relationship("Category", back_populates="budget_categories")


    # Serialize
    serialize_rules = ("-budget.budget_categories", "-category.budget_categories")

    @validates("budget_id")
    def validates_budget(self, _, budget):
        if not isinstance(budget, int):
            raise TypeError("Budget Id must be an integer")
        return budget
    
    @validates("category_id")
    def validates_category(self, _, category):
        if not isinstance(category, int):
            raise TypeError("Category Id must be an integer")
        return category
    
    @validates("allocated_amount")
    def validates_allocated_amount(self, _, allocated):
        if not isinstance(allocated, (float, int)):
             raise TypeError("Allocated amount must be a number")
        if allocated < 0:
            raise ValueError("Allocated Amount cannot be negative")
        return allocated
