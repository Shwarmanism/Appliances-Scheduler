from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from app.models import Appliances
import random

home = Blueprint('home', __name__)

@home.route('/dashboard')
@login_required
def home_dashboard():
    user_appliances = Appliances.query.filter_by(user_id=current_user.user_id).all()

    on_appliances = [a for a in user_appliances if a.status == 'on']
    total_kwh = sum(a.monthly_energy or 0 for a in on_appliances)
    estimated_cost = round(total_kwh * 6, 2)  # random value muna
    average_usage = round(total_kwh / len(on_appliances), 2) if on_appliances else 0

    top_appliances = sorted(on_appliances, key=lambda x: x.monthly_energy or 0, reverse=True)[:3]

    yesterday_usage = sum(a.daily_energy or 0 for a in on_appliances)

    notification = None
    if yesterday_usage > 35:
        notification = f"You exceeded your 5 kWh limit yesterday! ({round(yesterday_usage, 2)} kWh)"
        
    tips = [
        "Turn off appliances when not in use.",
        "Use LED lights to save energy.",
        "Avoid using high-wattage devices during peak hours.",
        "Unplug chargers when not in use.",
        "Wash clothes in cold water to save heating costs."
    ]
    random_tip = random.choice(tips)

    return render_template('dashboard.html',
                           total_kwh=round(total_kwh, 2),
                           estimated_cost=estimated_cost,
                           average_usage=average_usage,
                           top_appliances=top_appliances,
                           random_tip=random_tip,
                           notification=notification) 


# def total_monthly_cost():
    
# def peak_checker():
