from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from models import Appliances
from app import db

scheduler = Blueprint('scheduler', __name__)

# @scheduler.routes("/daily_scheduler", methods=['GET', 'POST'])
# @login_required
# def day_schedule():