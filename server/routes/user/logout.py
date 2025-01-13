from routes.__init__ import (
    Resource,
    make_response,
    unset_access_cookies,
    unset_refresh_cookies,
    jwt_required,
)


class Logout(Resource):
    @jwt_required()
    def delete(self):
        try:
            response = make_response({}, 204)
            unset_access_cookies(response)
            unset_refresh_cookies(response)
            return response
        except Exception as e:
            return make_response({"error": str(e)}, 422)