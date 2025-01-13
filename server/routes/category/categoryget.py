from routes.__init__ import make_response, Resource, jwt_required, request, db
from models.category import Category
from flask_jwt_extended import current_user

class CategoriesGet(Resource):
    @jwt_required()
    def get(self):
        try:
            # Fetch categories for the logged-in user
            categories = Category.query(user_id=current_user.id)

            # If no categories are found, return a message
            if not categories:
                return make_response({"message": "No categories found."}, 404)

            # Return the categories as a list of dictionaries
            return make_response([category.to_dict() for category in categories], 200)

        except Exception as e:
            return make_response({"error": str(e)}, 500)