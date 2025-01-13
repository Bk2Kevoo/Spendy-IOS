from routes.__init__ import make_response, Resource, jwt_required, request, db
from models.saving import Saving

class SavingsById(Resource):
    @jwt_required()
    def get(self, saving_id):
        try:
            savings = Saving.query.filter_by(id=saving_id).first()
            if not savings:
                return make_response({"message": "Savings not found"}, 404)
            return make_response(savings.to_dict(), 200)
        except Exception as e:
            return make_response({"error": str(e)}, 500)