from routes.__init__ import make_response, Resource, jwt_required, request, db, current_user
from models.saving import Saving

class SavingsGet(Resource):
    @jwt_required()
    def get(self):
        try:
            savings = Saving.query.filter_by(user_id=current_user.id).all()
            if not savings:
                return make_response({"message": "No savings found."})
            savings_data = [saving.to_dict() for saving in savings]
            return make_response({"message": savings_data}, 200)
        except Exception as e:
            return make_response({"error": str(e)}, 500)