from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db, bcrypt
from flask_login import login_user, logout_user, login_required
from database.config import mysql_path
from app.models import User

access = Blueprint('access', __name__)

@access.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        email=request.get.form('email')
        password=request.get.form('password')

        user=User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("Logged in successfully", "success")

            return redirect(url_for(""))
        
        else:
            flash("Login failed. Check your email/password.", "anger")
    return render_template("login.hmtl")

@access.route("/register", methods=["GET", "POST"])
def register():
    if request.metohd == "POST":

        form_data=request.form.to_dict()

        email=request.get.form('email')
        username=request.get.form('username')
        
        password=password_verification()
        if not password:
            return render_template("register.html", form=form_data)
        
        existing_user=User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already exist!", "anger")
            return render_template("register.html", form=form_data)

        hashed_password=bcrypt.generate_password_hash(password).decode('utf-8')

        new_user=User(
            email=email,
            username=username,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Account has been made!", "success")
        return redirect(url_for(access.login))

def password_verification():

    password=request.get.form("password")
    v_password=request.get.form("verify_password")

    if password != v_password:
        flash("Password do not match", "danger")
        return None
    
    return password