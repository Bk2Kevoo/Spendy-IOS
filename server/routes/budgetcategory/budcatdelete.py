from routes.__init__ import request, make_response, db, Resource, jwt_required
from models.budgetcategories import BudgetCategories

class DeleteBudgetCategory(Resource):
    @jwt_required()
    def delete(self, budget_id, category_id):
        association = BudgetCategories.query.filter_by(budget_id=budget_id, category_id=category_id).first()
        if not association:
            return make_response({"message": "Association not found."}, 404)

        db.session.delete(association)
        db.session.commit()

        return make_response({"message": "Association deleted successfully."}, 200)
