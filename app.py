from flask import Flask
from routes import main_routes
from models import db

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)

app.register_blueprint(main_routes)

if __name__ == '__main__':
    app.run(debug=True)
