from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import Appliances
from appliances_utils import AppliancesCatalog
from app import db
from uuid import uuid4

appliances = Blueprint('appliances', __name__)


@appliances.route('/appliances_tab', methods=['GET'])
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

    return render_template('appliances_tab.html', appliances=sorted_appliances)


@appliances.route('/add_appliance', methods=['GET', 'POST'])
@login_required
def add_appliances():
    if request.method == "POST":
        ave_monthly_bill = request.form.get('ave_monthly_bill')
        selected_appliance = request.form.get('selected_appliance')

        appliance_data = AppliancesCatalog.get_appliance_by_type(selected_appliance)

        if appliance_data:
            prefix = appliance_data.get('prefix', 'AP')
            appliances_id = generate_appliance_id(prefix)

            wattage_val = appliance_data['wattage']

            hours_used = request.form.get('hours_used')
            days_used = request.form.get('days_used')
            weeks_used = request.form.get('weeks_used')
            monthly_used = request.form.get('monthly_used')

            hourly_energy, daily_energy, weekly_energy, monthly_energy = energy_consumption(wattage_val, hours_used,
                                                                                          weeks_used, monthly_used)

            severity_level = severity_checker(daily_energy)

            new_appliance = Appliances(
                user_id=current_user.user_id,
                appliances_id=appliances_id,
                model=selected_appliance,
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
                status=None
            )

            db.session.add(new_appliance)
            db.session.commit()

            flash(f"Added {selected_appliance} with ID {appliances_id}!", "success")
            return redirect(url_for('appliances.add_appliances'))

        else:
            flash("Invalid appliance selected!", "danger")

    types_list = sorted(set(item['type'] for item in AppliancesCatalog.appliances)) 
    return render_template('appliances_tab.html', types=types_list)

def generate_appliance_id(category_prefix):
    return f"{category_prefix}-{uuid4().hex[:4].upper()}"

def energy_consumption(watt, hours, days, weeks):
    hourly_energy = watt / 1000
    daily_energy = (watt * hours) / 1000
    weekly_energy = (watt * hours * days) / 1000
    monthly_energy = (watt * hours * days * weeks) / 1000

    return float(hourly_energy), float(daily_energy), float(weekly_energy), float(monthly_energy)

def severity_checker(daily):
    if daily >= 1.5:
        return "Severe"
    elif 0.5 <= daily < 1.5:
        return "Moderate"
    else:
        return "Low"

