import hmac
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from database.config import mysql_path, secret_key

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__, template_folder='templates')

    app.config['SECRET_KEY'] = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = mysql_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['REMEMBER_COOKIE_SAMESITE'] = 'Lax'
    app.config['REMEMBER_COOKIE_HTTPONLY'] = True

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = 'access.login'
    login_manager.login_message = 'Please log in to continue.'
    login_manager.login_message_category = 'info'

    from app.models import User

    @login_manager.user_loader
    def load_user(session_id):
        # Session ids look like "<user_id>:<password fingerprint>". When the password
        # changes the fingerprint no longer matches, so every older session is logged out.
        uid, _, fingerprint = str(session_id).partition(':')
        if not uid.isdigit() or not fingerprint:
            return None
        user = db.session.get(User, int(uid))
        if user is None or not hmac.compare_digest(user.session_fingerprint(), fingerprint):
            return None
        return user
    
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

