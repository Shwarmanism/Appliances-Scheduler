from flask import Blueprint, render_templatee, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import Appliances
import seaborn as sns
import matplotlib.pyplot as plt
import io

analytics = Blueprint('analytics', __name__)

# @analytics.route("analytics_tab", methods=["GET", "POST"] )
# def analytics_t():


# def monthly_expenses():

# def comparison_to_last():

# def total_monthly_energy_consumption():

# def yearly_expenses_breakdown():

# def highest_expenses_yearly():

# def total_yearly_energy_consumption():

