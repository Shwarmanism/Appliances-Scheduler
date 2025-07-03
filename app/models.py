from app import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    fullname = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(254), nullable=False)

    def get_id(self):
        return str(self.user_id)
    
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

    start_hour = db.Column(db.Integer, nullable=False) 
    duration = db.Column(db.Integer, nullable=False)      
    cost = db.Column(db.Float, nullable=False)          
    energy_kwh = db.Column(db.Float, nullable=False)      
    is_partial = db.Column(db.Boolean, default=False)      
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    hours_used = db.Column(db.String(255))
    selected_type = db.Column(db.String(3), nullable=False)