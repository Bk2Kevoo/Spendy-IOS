from routes.__init__ import make_response, Resource, jwt_required, db
from models.budget import Budget
from flask_jwt_extended import current_user

class BudgetsDelete(Resource):
    @jwt_required()
    def delete(self, budget_id):
        try:
            budget = Budget.query.filter_by(id=budget_id, user_id=current_user.id).first()
            if not budget:
                return make_response({"error": "Budget not found or you do not have permission to delete it."}, 404)
            db.session.delete(budget)
            db.session.commit()
            return make_response({"message": "Budget deleted successfully."}, 200)
        except Exception as e:
            return make_response({"error": str(e)}, 500)
