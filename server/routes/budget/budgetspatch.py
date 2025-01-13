from routes.__init__ import make_response, Resource, jwt_required, request, db
from models.budget import Budget
from flask_jwt_extended import current_user

class BudgetPatch(Resource):
    @jwt_required()
    def patch(self, budget_id):
        try:
            data = request.get_json()
            budget = Budget.query.filter_by(id=budget_id, user_id=current_user.id).first()
            if not budget:
                return make_response({"message": "Budget not found or you do not have permission to update it."}, 404)

            if "name" in data:
                budget.name = data["name"]
            if "description" in data:
                budget.description = data["description"]
            if "total_amount" in data:
                budget.total_amount = data["total_amount"]
            if "start_date" in data:
                budget.start_date = data["start_date"]
            if "end_date" in data:
                budget.end_date = data["end_date"]
            if "category_id" in data:
                budget.category_id = data["category_id"]
            if "budget_type" in data:
                if data["budget_type"] in ['overall', 'monthly']:
                    budget.budget_type = data["budget_type"]
                else:
                    return make_response({"message": "Invalid budget type provided."}, 400)

            db.session.commit()
            return make_response(budget.to_dict(), 200)

        except Exception as e:
            return make_response({"error": str(e)}, 500)
