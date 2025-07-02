from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from app.models import Appliances, OptimizedAppliances, ScheduledApplianceUsage
import heapq
from app import db

import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import random

scheduler = Blueprint('scheduler', __name__)

@scheduler.route('/scheduling', methods=['GET', 'POST'])
@login_required
def schedule():
    appliances = Appliances.query.filter_by(user_id=current_user.user_id).all()

    schedule = {}
    total_cost = 0
    total_energy = 0
    plot_url = None
    selected_type = None
    selected_ids = None
    time_start = None
    time_end = None

    if request.method == 'POST':
        try:
            random.seed(42)  # optional: makes results reproducible

            hourly_rates = []
            for hour in range(24):
                if 0 <= hour < 6:
                    rate = round(random.uniform(3.0, 3.8), 2)  # Off-peak early morning
                elif 6 <= hour < 12:
                    rate = round(random.uniform(5.0, 6.5), 2)  # Morning ramp-up
                elif 12 <= hour < 18:
                    rate = round(random.uniform(6.5, 8.0), 2)  # Midday peak
                elif 18 <= hour < 22:
                    rate = round(random.uniform(7.0, 8.5), 2)  # Evening high
                else:
                    rate = round(random.uniform(4.0, 5.0), 2)  # Late evening cool-down
                hourly_rates.append(rate)

            selected_type = request.form.get('selected_type') 
            time_start = int(request.form.get('time_start') or 0)
            time_end = int(request.form.get('time_end') or 23)
            action_save = request.form.get('action_save')

            print("⏰ Received time range:")
            print("   time_start:", time_start)
            print("   time_end:", time_end)

            if selected_type == 'optimized':
                latest_combination = db.session.query(OptimizedAppliances.combination_id) \
                    .filter_by(user_id=current_user.user_id) \
                    .order_by(OptimizedAppliances.date_created.desc()) \
                    .first()

                if latest_combination:
                    combination_id = latest_combination.combination_id
                    selected_ids = [
                        entry.appliances_id
                        for entry in OptimizedAppliances.query
                        .filter_by(user_id=current_user.user_id, combination_id=combination_id)
                        .all()
                    ]
                else:
                    flash("No optimized combination found for your account.", "warning")
                    selected_ids = []
            else:
                selected_ids = request.form.getlist('selected_appliances')

            selected = [a for a in appliances if str(a.appliances_id) in selected_ids]
            
            for a in selected:
                if a.hours_used is None:
                    flash(f"No usage hours set for {a.model}.", "warning")
                    continue
                schedule[a.model] = dijkstra_schedule(
                    hourly_rates,
                    a.wattage,
                    a.hours_used,
                    time_start,
                    time_end
                )
            
            if selected_type == 'optimized' and action_save == 'save':
                for a in selected:
                    result = schedule.get(a.model)
                    if result:
                        energy_kwh = round((result['duration'] * a.wattage) / 1000, 2)
                        usage = ScheduledApplianceUsage(
                            user_id=current_user.user_id,
                            appliance_id=a.appliances_id,
                            start_hour=result['start_hour'],
                            duration=result['duration'],
                            cost=result['cost'],
                            energy_kwh=energy_kwh,
                            is_partial=result['is_partial'],
                            hours_used=",".join(str(h) for h in result['hours'])
                        )
                        db.session.add(usage)

                db.session.commit()
            
            total_cost = sum(info['cost'] for info in schedule.values())
            total_energy = sum(
                round((info['duration'] * appliance.wattage) / 1000, 2)
                for appliance in selected
                for model, info in schedule.items() if model == appliance.model
            )
            # plot_url = create_schedule_plot(schedule)

        except Exception as e:
            flash(f"An error occurred: {str(e)}", "danger")

    model_map = {a.appliances_id: a.model for a in appliances}

    latest_combination = db.session.query(OptimizedAppliances.combination_id) \
        .filter_by(user_id=current_user.user_id) \
        .order_by(OptimizedAppliances.date_created.desc()) \
        .first()

    optimized_appliances = []
    if latest_combination:
        combination_id = latest_combination.combination_id
        optimized_appliances = [
            entry.appliances_id for entry in OptimizedAppliances.query
            .filter_by(user_id=current_user.user_id, combination_id=combination_id).all()
        ]

    print("✅ POST received")
    print("📥 selected_type:", selected_type)
    print("📦 selected_appliances:", selected_ids)
    print("🕒 Time range:", time_start, "to", time_end)

    return render_template(
        'scheduling.html',
        appliances=appliances,
        schedule=schedule,
        total_cost=total_cost,
        total_energy=total_energy,
        plot_url=plot_url,
        on_appliances=[a for a in appliances if a.status == 'on'],
        model_map=model_map,
        optimized_appliances=optimized_appliances
    )

def dijkstra_schedule(rates, wattage, duration, time_start=0, time_end=23):
    # Handle wrap-around case like 19 (7 PM) to 13 (1 PM next day)
    valid_hours = []
    h = time_start
    while True:
        valid_hours.append(h % 24)
        if h % 24 == time_end % 24:
            break
        h += 1

    if len(valid_hours) < 1:
        return None

    actual_duration = min(duration, len(valid_hours))
    if actual_duration <= 0:
        return None

    costs = []
    for i in range(len(valid_hours) - actual_duration + 1):
        slot = valid_hours[i:i + actual_duration]
        cost = sum((wattage / 1000) * rates[h] for h in slot)
        costs.append((cost, slot[0], slot))

    if not costs:
        return None

    best_cost, best_start, best_hours = min(costs, key=lambda x: x[0])
    return {
        "start_hour": best_start,
        "duration": actual_duration,
        "cost": round(best_cost, 2),
        "hours": best_hours,
        "is_partial": actual_duration < duration
    }







# def create_schedule_plot(schedule_dict):
#     plt.figure(figsize=(10, 4))

#     for i, (name, info) in enumerate(schedule_dict.items()):
#         hours = info["hours"]
#         y = [i] * len(hours)
#         plt.scatter(hours, y, label=name, s=200)

#     plt.yticks(range(len(schedule_dict)), list(schedule_dict.keys()))
#     plt.xticks(range(24), [f"{h}:00" for h in range(24)])
#     plt.xlabel("Hour of Day")
#     plt.title("Optimal Appliance Usage Schedule")
#     plt.grid(True)
#     plt.legend(loc="upper right")

#     buf = io.BytesIO()
#     plt.tight_layout()
#     plt.savefig(buf, format="png")
#     buf.seek(0)
#     img_base64 = base64.b64encode(buf.read()).decode('utf-8')
#     buf.close()
#     return img_base64
