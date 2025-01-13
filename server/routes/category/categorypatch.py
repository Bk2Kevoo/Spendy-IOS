from routes.__init__ import make_response, Resource, jwt_required, request, db
from models.category import Category
from flask_jwt_extended import current_user

class CategoriesPatch(Resource):
    @jwt_required()
    def patch(self):
        try:
            # Get data from the request body
            data = request.get_json()

            # Ensure 'category_id' is provided in the request data
            if "category_id" not in data:
                return make_response({"error": "category_id is required."}, 400)

            # Fetch the category based on the provided category_id
            category = Category.query(id=data["category_id"], user_id=current_user.id)

            # Check if the category exists and belongs to the logged-in user
            if not category:
                return make_response({"error": "Category not found or you are not authorized to update this category."}, 404)

            # Update fields if present in the request data
            if "name" in data:
                category.name = data["name"]
            if "description" in data:
                category.description = data["description"]

            # Commit the changes to the database
            db.session.commit()

            # Return the updated category as a response
            return make_response(category.to_dict(), 200)

        except Exception as e:
            return make_response({"error": str(e)}, 500)
