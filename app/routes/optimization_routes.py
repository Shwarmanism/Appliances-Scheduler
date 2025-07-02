from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Appliances, OptimizedAppliances
from app import db
from datetime import datetime
from uuid import uuid4

optimizer = Blueprint('optimizer', __name__)

@optimizer.route('/optimize', methods=['GET', 'POST'])
@login_required
def optimize_appliances():
    print("[DEBUG] Entered /optimize route")

    user_appliances = Appliances.query.filter_by(user_id=current_user.user_id).all()
    print(f"[DEBUG] Retrieved {len(user_appliances)} appliances from DB")

    for a in user_appliances:
        if a.daily_energy is not None:
            if a.daily_energy >= 5:
                a.priority = 3
            elif a.daily_energy >= 2:
                a.priority = 2
            else:
                a.priority = 1
        else:
            a.priority = 0
        print(f"[DEBUG] Appliance: {a.model}, Daily Energy: {a.daily_energy}, Priority: {a.priority}")

    optimized = []
    total_energy = 0
    total_priority = 0
    cap = 0
    save_cost = 0

    if request.method == 'POST':
        try:
            cap_raw = request.form.get('energy-cap', '').strip()
            if not cap_raw:
                raise ValueError("Energy cap is empty.")
            cap = float(cap_raw)

            optimized = knapsack(user_appliances, cap)
            print(f"[DEBUG] Optimized appliances selected: {[a.model for a in optimized]}")

            total_energy = sum(a.daily_energy for a in optimized)
            total_priority = sum(a.priority for a in optimized)
            save_cost = total_save(user_appliances, optimized)

            print(f"[DEBUG] Total Energy: {total_energy} kWh")
            print(f"[DEBUG] Total Priority Score: {total_priority}")
            print(f"[DEBUG] Estimated Savings: ₱{save_cost}")

            save_process = request.form.get('save_not')
            if save_process == "save":
                combination_id = f'Combi-{uuid4().hex[:4]}'
                print(f"[DEBUG] Saving optimized combination with ID: {combination_id}")

                for appliance in optimized:
                    print(f"[DEBUG] Saving appliance: {appliance.model} to DB")
                    entry = OptimizedAppliances(
                        user_id=current_user.user_id,
                        combination_id=combination_id,
                        appliances_id=appliance.appliances_id,
                        date_created=datetime.now()
                    )
                    db.session.add(entry)
                db.session.commit()
                print("[DEBUG] Optimized combination saved to DB")

        except ValueError as e:
            print(f"[ERROR] Invalid input for energy cap: {e}")
            flash("Please enter a valid energy capacity.", "danger")

    return render_template('optimization.html',
                           appliances=optimized,
                           energy_cap=cap,
                           total_energy=total_energy,
                           total_priority=total_priority,
                           save_cost=save_cost)

def knapsack(appliances, max_kwh):
    n = len(appliances)
    W = int(max_kwh * 100) #Converting the cap size into integer to prevent float-based error lang
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        wt = int((appliances[i-1].daily_energy or 0) * 100)
        val = appliances[i-1].priority
        for w in range(W + 1):
            if wt <= w:
                dp[i][w] = max(dp[i-1][w], val + dp[i-1][w - wt])
            else:
                dp[i][w] = dp[i-1][w]

    selected = []
    w = W
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected.append(appliances[i-1])
            w -= int((appliances[i-1].daily_energy or 0) * 100)

    return selected[::-1]

def total_save(appliances, selected_appliances):

    all_on = [a for a in appliances if a.status == 'on']
    total_cost_all = sum((a.daily_energy or 0) * 11 for a in all_on)

    total_cost_selected = sum((a.daily_energy or 0) * 11 for a in selected_appliances)

    savings = round(total_cost_all - total_cost_selected, 2)

    return savings

