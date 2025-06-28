from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from database.config import mysql_path, secret_key

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='templates')

    app.config['SECRET_KEY'] = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = mysql_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'info'

    from app.routes.login_routes import access
    from app.routes.home_routes import home
    from app.routes.appliances_routes import appliances
    from app.routes.analytics_routes import analytics

    app.register_blueprint(access)
    app.register_blueprint(home)
    app.register_blueprint(appliances)
    app.register_blueprint(analytics)

    return app
