from datetime import datetime
from flask import Blueprint, render_template, flash, url_for
from sqlalchemy import func
from flask_login import login_required, current_user
from app import db, rates
from app.models import Appliances, OptimizedAppliances, ScheduledApplianceUsage, unique_appliance_names
import random

home = Blueprint('home', __name__)

@home.route('/dashboard')
@login_required
def home_dashboard():
    uid = current_user.user_id
    user_appliances = Appliances.query.filter_by(user_id=uid).all()
    by_id = {a.appliances_id: a for a in user_appliances}
    names = unique_appliance_names(user_appliances)
    on_appliances = [a for a in user_appliances if a.status == 'on']

    total_kwh = sum(a.monthly_energy or 0 for a in on_appliances)
    daily_kwh = sum(a.daily_energy or 0 for a in on_appliances)
    estimated_cost = round(total_kwh * rates.ESTIMATE_RATE, 2)

    # Every appliance, heaviest first, so it can be switched on or off from here.
    ranked = sorted(user_appliances, key=lambda a: a.monthly_energy or 0, reverse=True)[:5]

    # Latest saved schedule: the rows from the most recent save share one timestamp.
    latest_at = db.session.query(func.max(ScheduledApplianceUsage.date_created)).filter_by(user_id=uid).scalar()
    schedule = []
    saved_day = saved_month = 0.0
    if latest_at:
        rows = ScheduledApplianceUsage.query.filter_by(user_id=uid, date_created=latest_at).all()
        for r in rows:
            a = by_id.get(r.appliance_id)
            if not a:
                continue  # appliance was deleted after the schedule was saved
            hours = [int(h) for h in (r.hours_used or '').split(',') if h.strip().isdigit()]
            peak_cost = (r.energy_kwh or 0) * rates.PEAK_RATE
            save = max(peak_cost - (r.cost or 0), 0)
            saved_day += save
            saved_month += save * (a.days_used or 0) * (a.weeks_used or 0)
            schedule.append({
                'name': names[a.appliances_id], 'hours': hours, 'start': r.start_hour,
                'end': (r.start_hour + r.duration) % 24, 'duration': r.duration,
                'cost': r.cost or 0, 'partial': r.is_partial,
            })
        schedule.sort(key=lambda x: ((x['start'] - rates.PEAK_END) % 24, x['name']))

    has_plan = OptimizedAppliances.query.filter_by(user_id=uid).first() is not None
    steps = [
        ('Add your appliances', bool(user_appliances), url_for('appliances.appliances_display')),
        ('Switch on the ones you use', bool(on_appliances), url_for('appliances.appliances_display')),
        ('Build an optimized plan', has_plan, url_for('optimizer.optimize_appliances')),
        ('Save a schedule', bool(schedule), url_for('scheduler.schedule')),
    ]

    notification = None
    if daily_kwh > rates.DAILY_LIMIT_KWH:
        notification = (f"Your switched-on appliances add up to about {daily_kwh:.1f} kWh a day, "
                        f"over the {rates.DAILY_LIMIT_KWH} kWh daily guide.")

    return render_template('dashboard.html',
                           total_kwh=round(total_kwh, 1),
                           estimated_cost=estimated_cost,
                           ranked=ranked,
                           usage_json={a.appliances_id: {'kwh': a.monthly_energy or 0, 'on': a.status == 'on'}
                                       for a in user_appliances},
                           on_count=len(on_appliances),
                           all_count=len(user_appliances),
                           schedule=schedule,
                           schedule_saved_at=latest_at if schedule else None,
                           saved_day=round(saved_day, 2),
                           saved_month=round(saved_month, 2),
                           steps=steps,
                           tip=smart_tip(on_appliances, total_kwh, names, {s['name'] for s in schedule}),
                           notification=notification,
                           now_hour=datetime.now().hour)


def smart_tip(on_appliances, total_kwh, names, scheduled_names):
    """One tip, worked out from the user's own heaviest appliance."""
    if not on_appliances or not total_kwh:
        return random.choice(GENERIC_TIPS)
    top = max(on_appliances, key=lambda a: a.monthly_energy or 0)
    name = names[top.appliances_id]
    share = round((top.monthly_energy or 0) / total_kwh * 100)
    hours = top.hours_used or 0
    kw = (top.wattage or 0) / 1000
    if hours > rates.OFFPEAK_HOURS or name in scheduled_names:
        save = kw * rates.PEAK_RATE
        why = "already runs off-peak" if name in scheduled_names else f"runs {hours} h a day, longer than the off-peak window"
        return (f"{name} is {share}% of your monthly use and {why}. "
                f"Using it one hour less a day saves about ₱{save:,.2f} a day.")
    save = (top.daily_energy or 0) * (rates.PEAK_RATE - rates.OFFPEAK_RATE)
    return (f"{name} is {share}% of your monthly use. Running it off-peak "
            f"({rates.hour_label(rates.PEAK_END)} – {rates.hour_label(rates.PEAK_START)}) instead of at peak "
            f"saves about ₱{save:,.2f} a day.")


GENERIC_TIPS = [
    "Turn off appliances when not in use.",
    "Use LED lights to save energy.",
    "Avoid using high-wattage devices during peak hours.",
    "Unplug chargers when not in use.",
    "Wash clothes in cold water to save heating costs.",
]


# def total_monthly_cost():
    
# def peak_checker():
