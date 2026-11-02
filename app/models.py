from app import db
from flask_login import UserMixin
from datetime import datetime
import hashlib
import hmac
from flask import current_app

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    fullname = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(254), nullable=False)

    def session_fingerprint(self):
        # Keyed digest of the stored password hash: changes whenever the password does,
        # and never exposes the hash itself in the session cookie.
        key = current_app.config['SECRET_KEY'].encode()
        return hmac.new(key, self.password.encode(), hashlib.sha256).hexdigest()[:32]

    def get_id(self):
        return f"{self.user_id}:{self.session_fingerprint()}"
    
    appliances = db.relationship(
        'Appliances',
        backref='user',
        lazy=True,
        cascade='all, delete-orphan'
    )

class Appliances(db.Model):
    __tablename__ = 'appliances'

    appliances_id = db.Column(db.String(25), primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    model = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(30), nullable=False)
    capacity = db.Column(db.String(30), nullable=False)
    wattage = db.Column(db.Integer, nullable=False)

    severity_level = db.Column(db.String(20), nullable=False)
    hours_used = db.Column(db.Integer, nullable=False)
    hourly_energy = db.Column(db.Float, nullable=False)
    days_used = db.Column(db.Integer, nullable=False)
    daily_energy = db.Column(db.Float, nullable=False)
    weeks_used = db.Column(db.Integer, nullable=False)
    weekly_energy = db.Column(db.Float, nullable=False)
    monthly_used = db.Column(db.Integer, nullable=False)
    monthly_energy = db.Column(db.Float, nullable=False)

    status = db.Column(db.String(3), default='off', nullable=False)

class OptimizedAppliances(db.Model):
    __tablename__=('optimized_appliances')

    optimized_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    combination_id = db.Column(db.Integer, nullable=False)
    appliances_id = db.Column(db.String(25), db.ForeignKey('appliances.appliances_id'), nullable=False)
    date_created = db.Column(db.Date, nullable=False)

class ScheduledApplianceUsage(db.Model):
    __tablename__ = 'scheduled_appliances'

    scheduled_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    appliance_id = db.Column(db.String(25), db.ForeignKey('appliances.appliances_id'), nullable=False)

    start_hour = db.Column(db.Integer, nullable=False)       # 0–23
    duration = db.Column(db.Integer, nullable=False)         # in hours
    cost = db.Column(db.Float, nullable=False)               # ₱ value
    energy_kwh = db.Column(db.Float, nullable=False)         # kWh
    is_partial = db.Column(db.Boolean, default=False)        # if only partially scheduled
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Optional: store raw list of hours as comma-separated string (e.g. "5,6,7,...")
    hours_used = db.Column(db.String(255))