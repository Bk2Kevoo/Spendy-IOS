from routes.__init__ import make_response, Resource, jwt_required, request, db
from models.category import Category
from flask_jwt_extended import current_user

class CategoriesDelete(Resource):
    @jwt_required()
    def delete(self):
        try:
            # Get the category ID or name from the request body (based on your design)
            data = request.get_json()
            
            if "category_id" not in data:
                return make_response({"error": "category_id is required."}, 400)

            # Fetch the category by ID
            category = Category.query.get(data["category_id"])

            # Check if the category exists and belongs to the logged-in user
            if not category or category.user_id != current_user.id:
                return make_response({"error": "Category not found or you are not authorized to delete this category."}, 403)

            # Delete the category
            db.session.delete(category)
            db.session.commit()

            # Return a success message
            return make_response({"message": "Category deleted successfully."}, 200)

        except Exception as e:
            return make_response({"error": str(e)}, 500)
