from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_required, current_user
import seaborn as sns
import matplotlib.pyplot as plt
import io

home = Blueprint('home', __name__)

# @home.route("/home_tab", methods=["GET","POST"])
# def home_t():


# def total_electricity_cost():

# def ave_usage_for_month():

# def application_used_today():

# def consumption_report():
