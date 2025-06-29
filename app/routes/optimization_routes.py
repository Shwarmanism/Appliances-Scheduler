from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Appliances
from app import db

optimizer = Blueprint('optimizer', __name__)

def knapsack(appliances, max_kwh):
    n = len(appliances)
    W = int(max_kwh * 100)
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

@optimizer.route('/optimize', methods=['GET', 'POST'])
@login_required
def optimize_appliances():
    user_appliances = Appliances.query.filter_by(user_id=current_user.user_id).all()

    for a in user_appliances:
        if a.daily_energy is not None:
            if a.daily_energy >= 1.5:
                a.priority = 3
            elif a.daily_energy >= 0.8:
                a.priority = 2
            else:
                a.priority = 1
        else:
            a.priority = 0

    optimized = []
    total_energy = 0
    total_priority = 0
    cap = 0

    if request.method == 'POST':
        try:
            cap = float(request.form.get('energy_cap'))
            optimized = knapsack(user_appliances, cap)
            total_energy = sum(a.daily_energy for a in optimized)
            total_priority = sum(a.priority for a in optimized)
        except ValueError:
            flash("Please enter a valid energy capacity.", "danger")

    return render_template('optimize_tab.html',
                           appliances=optimized,
                           energy_cap=cap,
                           total_energy=total_energy,
                           total_priority=total_priority)