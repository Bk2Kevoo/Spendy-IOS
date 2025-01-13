from routes.__init__ import request, make_response, db, Resource, jwt_required
from models.budgetcategories import BudgetCategories

class AddBudgetCategory(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        budget_id = data.get("budget_id")
        category_id = data.get("category_id")

        if not budget_id or not category_id:
            return make_response({"message": "Budget ID and Category ID are required."}, 400)

        # Check for duplicates
        existing = BudgetCategories.query.filter_by(budget_id=budget_id, category_id=category_id).first()
        if existing:
            return make_response({"message": "Association already exists."}, 400)

        new_association = BudgetCategories(budget_id=budget_id, category_id=category_id)
        db.session.add(new_association)
        db.session.commit()

        return make_response({"message": "Association created successfully."}, 201)
