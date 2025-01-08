from models.__init__ import SerializerMixin, db, validates
from datetime import datetime

class Category(db.Model, SerializerMixin):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f"""
            <Category #{self.id}: 
                Name: {self.name},
                Description: {self.description}
                Default: {self.is_default}
                Created At: {self.created_at}
                Updated At: {self.updated_at}>
        """
    
    # Relationships
    budget_categories = db.relationship("BudgetCategories", back_populates="category")

    # Serialize
    serialize_rules = ("-budget_categories",)

    @validates("name")
    def validate_name(self, _, name):
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        if len(name) < 3:
            raise ValueError("Name must be at least 3 characters long.")
        return name

    @validates("description")
    def validate_description(self, _, description):
        if description and not isinstance(description, str):
            raise TypeError("Description must be a string.")
        return description

    @validates("is_default")
    def validate_is_default(self, _, is_default):
        if not isinstance(is_default, bool):
            raise TypeError("is_default must be a boolean value.")
        return is_default

    @validates("created_at")
    def validate_created_at(self, _, created_at):
        if created_at and not isinstance(created_at, datetime):
            raise TypeError("Created At must be a datetime object.")
        return created_at

    @validates("updated_at")
    def validate_updated_at(self, _, updated_at):
        if updated_at and not isinstance(updated_at, datetime):
            raise TypeError("Updated At must be a datetime object.")
        return updated_at
