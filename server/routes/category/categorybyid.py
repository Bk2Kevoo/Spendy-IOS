from routes.__init__ import make_response, Resource, jwt_required, request, db
from models.category import Category
from flask_jwt_extended import current_user


class CategoriesById(Resource):
    @jwt_required()
    def get(self, category_id):
        try:
            category = Category.query.filter_by(id=category_id, user_id=current_user.id).first()
            if not category:
                return make_response({"message": "No category found or you do not have access to this."})
            return make_response(category.dict(), 200)
        except Exception as e:
            return make_response({"error": str(e)}, 500)