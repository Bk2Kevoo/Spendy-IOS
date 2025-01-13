from werkzeug.exceptions import NotFound
from config import app, api

# From my User Foler
from routes.user.login import Login
from routes.user.currentuser import CurrentUser
from routes.user.currentuser import CurrentUserPatch
from routes.user.googlesignin import GoogleAuth
from routes.user.logout
from routes.user.recoverpassword
from routes.user.refresh
from routes.user.signup



# All Routes






if __name__ == '__main__':
    app.run(port=5555, debug=True)

