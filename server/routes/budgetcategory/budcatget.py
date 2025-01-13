from routes.__init__ import request, make_response, db, Resource, jwt_required
from models.budgetcategories import BudgetCategories


class GetCategoriesForBudget(Resource):
    @jwt_required()
    def get(self, budget_id):
        categories = BudgetCategories.query.filter_by(budget_id=budget_id).all()
        if not categories:
            return make_response({"message": "No categories found for this budget."}, 404)

        return make_response(
            {"categories": [category.to_dict() for category in categories]}, 
            200
        )
