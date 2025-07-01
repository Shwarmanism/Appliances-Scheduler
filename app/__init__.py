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

    login_manager.login_view = 'access.login'
    login_manager.login_message = 'info'

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    @app.template_filter('format_hour')
    def format_hour(hour):
        if hour is None:
            return "Invalid hour"
        try:
            hour = int(hour) % 24
            suffix = "AM" if hour < 12 else "PM"
            display = hour % 12
            if display == 0:
                display = 12
            return f"{display}:00 {suffix}"
        except (ValueError, TypeError):
            return "Invalid hour"

    from app.routes.login_routes import access
    from app.routes.home_routes import home
    from app.routes.appliances_routes import appliances
    from app.routes.analytics_routes import analytics
    from app.routes.optimization_routes import optimizer
    from app.routes.daily_scheduler_routes import scheduler

    app.register_blueprint(access)
    app.register_blueprint(home)
    app.register_blueprint(appliances, url_prefix='/appliances')
    app.register_blueprint(optimizer)
    app.register_blueprint(scheduler)
    app.register_blueprint(analytics)

    return app

