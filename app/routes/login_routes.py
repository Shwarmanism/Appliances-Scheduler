from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app import db, bcrypt
from app.models import User 

access = Blueprint('access', __name__)

@access.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("Logged in successfully", "success")
            return redirect(url_for("home.home_dashboard"))
        else:
            flash("Login failed. Check your email/password.", "danger")

    return render_template("login.html")

@access.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        form_data = request.form.to_dict()
        
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        username = request.form.get('username')

        password = password_verification()
        if not password:
            return render_template("register.html", form=form_data)

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already exists!", "danger")
            return render_template("register.html", form=form_data)

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(
            fullname=fullname,
            email=email,
            username=username,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Account has been created!", "success")
        return redirect(url_for('access.login'))

    return render_template("register.html")

def password_verification():
    password = request.form.get("password")
    v_password = request.form.get("verify_password")

    if password != v_password:
        flash("Passwords do not match.", "danger")
        return None

    return password
