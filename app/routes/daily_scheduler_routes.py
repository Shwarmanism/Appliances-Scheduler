from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from app.models import Appliances
import heapq
from app import db

import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

scheduler = Blueprint('scheduler', __name__)

@scheduler.route('/scheduling', methods=['GET', 'POST'])
@login_required
def schedule():
    appliances = Appliances.query.filter_by(user_id=current_user.user_id).all()
    schedule = {}
    
    if request.method == 'POST':
        hourly_rates = [float(request.form.get(f"rate_{i}")) for i in range(24)]
        selected_ids = request.form.getlist('selected_appliances')
        duration_dict = {aid: int(request.form.get(f'duration_{aid}')) for aid in selected_ids}
        time_start = int(request.form.get('time_start') or 0)
        time_end = int(request.form.get('time_end') or 23)

        selected = [a for a in appliances if a.appliances_id in selected_ids]

        for a in selected:
            schedule[a.model] = dijkstra_schedule(hourly_rates, a.wattage, duration_dict[a.appliances_id], time_start, time_end)

        plot_url = create_schedule_plot(schedule)

    return render_template('daily_scheduler.html', appliances=appliances, schedule=schedule, plot_url=plot_url)

def dijkstra_schedule(rates, wattage, duration, time_start=0, time_end=23):
    costs = []
    for start in range(time_start, time_end - duration + 2):
        total_cost = 0
        for h in range(start, start + duration):
            total_cost += (wattage / 1000) * rates[h % 24]
        costs.append((total_cost, start))

    costs.sort()
    best_cost, best_start = costs[0]
    best_range = [(best_start + i) % 24 for i in range(duration)]
    return {
        "start_hour": best_start,
        "duration": duration,
        "cost": round(best_cost, 2),
        "hours": best_range
    }

def create_schedule_plot(schedule_dict):
    plt.figure(figsize=(10, 4))

    for i, (name, info) in enumerate(schedule_dict.items()):
        hours = info["hours"]
        y = [i] * len(hours)
        plt.scatter(hours, y, label=name, s=200)

    plt.yticks(range(len(schedule_dict)), list(schedule_dict.keys()))
    plt.xticks(range(24), [f"{h}:00" for h in range(24)])
    plt.xlabel("Hour of Day")
    plt.title("Optimal Appliance Usage Schedule")
    plt.grid(True)
    plt.legend(loc="upper right")

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return img_base64
