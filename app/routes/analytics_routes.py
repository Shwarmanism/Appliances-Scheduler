from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import Appliances
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64

analytics = Blueprint('analytics', __name__)

@analytics.route("/analytics", methods=["GET", "POST"] )
@login_required
def analytics_tab():

    user_appliances = Appliances.query.filter_by(user_id=current_user.user_id).all()
    total_appliances = 0
    total_daily_kwh = 0
    total_monthly_kwh = 0
    total_monthly_cost = 0
    plot_url = None

    if request.method == 'POST':
        total_appliances = len(user_appliances)
        total_daily_kwh = sum(user_appliances.daily_energy)
        total_monthly_kwh = sum(user_appliances.monthly_energy)
        total_monthly_cost = round(total_monthly_kwh * 6, 2)

        plot_url = appliances_usage_breakdown(user_appliances)


    return render_template("analytics.html",
                           total_appliances=total_appliances,
                           total_daily_kwh=total_daily_kwh,
                           total_monthly_cost=total_monthly_cost,
                           plot_url=plot_url)



def appliances_usage_breakdown(appliances):
    labels = [a.model for a in appliances]
    usage_values = [a.daily_energy or 0 for a in appliances]

    filtered_data = [(label, usage) for label, usage in zip(labels, usage_values) if usage > 0]
    if not filtered_data:
        return None 

    labels, usage_values = zip(*filtered_data)

    plt.figure(figsize=(8, 8))
    plt.pie(
        usage_values,
        labels=labels,
        autopct='%1.1f%%',
        startangle=140,
        colors=sns.color_palette("crest", len(labels))
    )
    plt.title("Appliance Daily Energy Usage Breakdown", fontsize=14)
    plt.axis('equal') 

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()

    return encoded

# def saving_chart(appliance):
    

