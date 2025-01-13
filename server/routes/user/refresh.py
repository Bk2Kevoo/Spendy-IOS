from routes.__init__ import (
    Resource,
    make_response,
    create_access_token,
    set_access_cookies,
    jwt_required,
    current_user
)


class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        try:
            access_token = create_access_token(identity=current_user.id)
            response = make_response(current_user.to_dict(), 200)
            set_access_cookies(response, access_token)
            return response
        except Exception as e:
            return make_response({"error": str(e)}, 422)