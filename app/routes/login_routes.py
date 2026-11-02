from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
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


@access.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("You've been logged out.", "success")
    return redirect(url_for("access.login"))


@access.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        action = request.form.get("action")

        if action == "profile":
            fullname = (request.form.get("fullname") or "").strip()
            email = (request.form.get("email") or "").strip()
            email_changed = email.lower() != (current_user.email or "").lower()
            if not fullname or not email:
                flash("Name and email can't be empty.", "danger")
            elif email_changed and not bcrypt.check_password_hash(
                    current_user.password, request.form.get("current_password") or ""):
                flash("Enter your current password to change your email.", "danger")
            elif email_changed and User.query.filter_by(email=email).first():
                flash("That email is already used by another account.", "danger")
            else:
                current_user.fullname = fullname
                current_user.email = email
                db.session.commit()
                flash("Profile updated.", "success")

        elif action == "password":
            old = request.form.get("old_password") or ""
            new = request.form.get("new_password") or ""
            confirm = request.form.get("confirm_password") or ""
            if not bcrypt.check_password_hash(current_user.password, old):
                flash("Your current password is incorrect.", "danger")
            elif not new:
                flash("Enter a new password.", "danger")
            elif new != confirm:
                flash("New passwords do not match.", "danger")
            else:
                current_user.password = bcrypt.generate_password_hash(new).decode("utf-8")
                db.session.commit()
                # The session id includes a fingerprint of the password hash, so every
                # other session is now invalid. Re-issue this one so the user stays in.
                user = current_user._get_current_object()
                logout_user()
                session.clear()
                login_user(user)
                flash("Password changed. Other devices have been logged out.", "success")

        return redirect(url_for("access.settings"))

    return render_template("settings.html")
