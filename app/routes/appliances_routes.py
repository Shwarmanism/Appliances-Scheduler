from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from app.models import Appliances
from app.appliances_utils import AppliancesCatalog
from app import db
from uuid import uuid4
import ast

appliances = Blueprint('appliances', __name__)

@appliances.route('/', methods=['GET'])
@login_required
def appliances_display():
    user_appliances = Appliances.query.filter_by(user_id=current_user.user_id).all()

    sorted_appliances = []
    for appliance in user_appliances:
        inserted = False
        for i in range(len(sorted_appliances)):
            if (appliance.daily_energy or 0) > (sorted_appliances[i].daily_energy or 0):
                sorted_appliances.insert(i, appliance)
                inserted = True
                break
        if not inserted:
            sorted_appliances.append(appliance)

    types_list = sorted(set(item['type'] for item in AppliancesCatalog.appliances))

    return render_template(
        'appliances.html',
        appliances=sorted_appliances,
        types=types_list,
        catalog=AppliancesCatalog.appliances
    )

@appliances.route('/toggle_appliance_status', methods=['POST'])
@login_required
def toggle_appliance_status():
    appliance_id = request.form.get('appliance_id')
    new_status = request.form.get('status')

    appliance = Appliances.query.filter_by(user_id=current_user.user_id, appliances_id=appliance_id).first()
    if appliance:
        appliance.status = new_status
        db.session.commit()
        return jsonify(success=True), 200
    return jsonify(success=False), 404

@appliances.route('/add_appliance', methods=['POST'])
@login_required
def add_appliances():

    appliance_model = request.form.get('appliance-model')
    hours_used = int(request.form.get('appliance-hours', 1))
    
    days_str = request.form.get('appliance-days', '[]')
    try:
        days_used = len(ast.literal_eval(days_str))
    except (ValueError, SyntaxError):
        days_used = 0

    weeks_used = int(request.form.get('appliance-weeks', 4))
    monthly_used = weeks_used

    appliance_id = request.form.get('appliance-select')
    appliance_data = AppliancesCatalog.get_appliance_by_id(appliance_id)

    if appliance_data:
        prefix = appliance_data.get('prefix', 'AP') 
        appliances_id = generate_appliance_id(prefix)

        wattage_val = float(appliance_data['wattage'])

        hourly_energy, daily_energy, weekly_energy, monthly_energy = energy_consumption(
            wattage_val, hours_used, days_used, weeks_used
        )

        severity_level = severity_checker(daily_energy)

        new_appliance = Appliances(
            user_id=current_user.user_id,
            appliances_id=appliances_id,
            model=appliance_model,
            category=appliance_data['category'],
            capacity=appliance_data['capacity'],
            wattage=wattage_val,
            severity_level=severity_level,
            hours_used=hours_used,
            hourly_energy=hourly_energy,
            days_used=days_used,
            daily_energy=daily_energy,
            weeks_used=weeks_used,
            weekly_energy=weekly_energy,
            monthly_used=monthly_used,
            monthly_energy=monthly_energy,
            status='off'
        )   

        print("🔍 DEBUGGING new_appliance FIELDS:")
        for attr in [
            'user_id', 'appliances_id', 'model', 'category', 'capacity', 'wattage',
            'severity_level', 'hours_used', 'hourly_energy', 'days_used',
            'daily_energy', 'weeks_used', 'weekly_energy', 'monthly_used',
            'monthly_energy', 'status'
        ]:
            print(f"{attr}: {getattr(new_appliance, attr)}")

        try:
            db.session.add(new_appliance)
            db.session.commit()
            print("Saved successfully!")
        except Exception as e:
            print("DB error occurred:", e)
            db.session.rollback()
            flash("Database error: " + str(e), "danger")

        flash(f"Added {appliance_model} with ID {appliances_id}!", "success")
    else:
        flash("Invalid appliance selected!", "danger")

    print("🔧 Reached add_appliances POST route")
    return redirect(url_for('appliances.appliances_display'))


@appliances.route('/delete_appliance/<string:appliance_id>', methods=['POST'])
@login_required
def delete_appliance(appliance_id):
    appliance = Appliances.query.filter_by(user_id=current_user.user_id, appliances_id=appliance_id).first()

    if appliance:
        db.session.delete(appliance)
        db.session.commit()
        flash(f"Appliance {appliance.model} has been deleted.", "success")
    else:
        flash("Appliance not found.", "danger")

    return redirect(url_for('appliances.appliances_display'))

def generate_appliance_id(category_prefix):
    return f"{category_prefix}-{uuid4().hex[:4].upper()}"

def energy_consumption(watt, hours, days, weeks):
    hourly_energy = watt / 1000
    daily_energy = (watt * hours) / 1000
    weekly_energy = (watt * hours * days) / 1000
    monthly_energy = (watt * hours * days * weeks) / 1000

    return float(hourly_energy), float(daily_energy), float(weekly_energy), float(monthly_energy)

def severity_checker(daily):
    if daily > 5:
        return "Severe"
    elif 2 <= daily <= 5:
        return "Moderate"
    else:
        return "Low"
