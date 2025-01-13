from routes.__init__ import make_response, Resource, jwt_required, request, db, current_user
from models.saving import Saving

class SavingsDelete(Resource):
    @jwt_required()
    def delete(self, saving_id):
        try:
            savings = Saving.query.filter_by(id=saving_id, user_id=current_user.id).first()
            if not savings:
                return make_response({"message": "Saving not found."}, 404)
            db.session.delete(savings)
            db.session.commit()
            return make_response({"message": "Savings deleted successfully."}, 200)
        except Exception as e:
            return make_response({"error": str(e)}, 500)