from routes.__init__ import make_response, Resource, jwt_required, request, db
from models.budget import Budget
from flask_jwt_extended import current_user

class BudgetsById(Resource):
    @jwt_required()
    def get(self, budget_id):
        try:
            budget = Budget.query.filter_by(id=budget_id, user_id=current_user.id).first()
            if not budget:
                return make_response({"message": "Budget not found or you do not have permission to access it."}, 404)
            return make_response(budget.to_dict(), 200)
        except Exception as e:
            return make_response({"error": str(e)}, 500)
