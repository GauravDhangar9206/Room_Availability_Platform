from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.extensions import db
from app.models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        fullname = request.form.get("fullname")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        role = request.form.get("role")

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("auth.signup"))

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already exists!", "danger")
            return redirect(url_for("auth.signup"))

        # Create new user
        user = User(
            fullname=fullname,
            email=email,
            phone=phone,
            role=role
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Registration Successful! Please Login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/signup.html")


@auth_bp.route("/login")
def login():
    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    return redirect(url_for("home.index"))