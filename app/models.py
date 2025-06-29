from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    appliances = db.relationship('Appliances', backref='user', lazy=True)

class Appliances(db.Model):
    __tablename__ = 'appliances'

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    appliances_id = db.Column(db.String(25), primary_key=True)
    model = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(15), nullable=False)
    capacity = db.Column(db.String(15), nullable=False)
    wattage = db.Column(db.Integer, nullable=False)
    severity_level = db.Columnt(db.String(15), nullable=False)
    hours_used = db.Column(db.Integer, nullable=False)
    hourly_energy = db.Column(db.Integer, nulable=False)
    days_used = db.Column(db.Integer, nullable=False)
    daily_energy = db.Column(db.Integer, nulable=False)
    weeks_used = db.Column(db.Integer, nullable=False)
    weekly_energy = db.Column(db.Integer, nulable=False)
    monthly_used = db.Column(db.Integer, nullable=False)
    monthly_energy = db.Column(db.Integer, nulable=False)
