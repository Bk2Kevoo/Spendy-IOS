from routes.__init__ import make_response, Resource, jwt_required, request, db
from models.category import Category
from flask_jwt_extended import current_user

class CategoriesPost(Resource):
    @jwt_required()
    def post(self):
        try:
            # Get data from the request body
            data = request.get_json()

            # Check if required fields are present
            if "name" not in data or "description" not in data:
                return make_response({"error": "Name and description are required."}, 400)

            # Create a new category instance for the logged-in user
            new_category = Category(
                name=data["name"],
                description=data["description"],
                user_id=current_user.id  # Associate the category with the logged-in user
            )

            # Add the new category to the database and commit the transaction
            db.session.add(new_category)
            db.session.commit()

            # Return the created category as a response
            return make_response(new_category.to_dict(), 201)

        except Exception as e:
            return make_response({"error": str(e)}, 500)
