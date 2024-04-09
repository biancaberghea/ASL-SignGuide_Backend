from RestAPI.app import app
from RestAPI.controller.profile import profile_bp

app.app_context().push()

from RestAPI.controller.auth import auth_bp
from RestAPI.controller.categories import cat_bp
app.register_blueprint(auth_bp)
app.register_blueprint(cat_bp)
app.register_blueprint(profile_bp)

if __name__ == '__main__':
    app.run(debug=True)
