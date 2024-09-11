from flask import Flask
from routes import auth, main_routes 
from models import db, User
from flask_login import LoginManager


app = Flask(__name__)

# Configure the app (database and secret key)
app.config.from_object('config.Config')

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # Set the login route

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register the blueprints
app.register_blueprint(main_routes)
app.register_blueprint(auth, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True)
