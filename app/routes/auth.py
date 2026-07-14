from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from app.extensions import db
from app.models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# ----------------------------
# Signup
# ----------------------------
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():

    # If user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for("home.index"))

    if request.method == "POST":

        fullname = request.form.get("fullname").strip()
        email = request.form.get("email").strip().lower()
        phone = request.form.get("phone").strip()
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        role = request.form.get("role")

        # Check required fields
        if not fullname or not email or not password or not role:
            flash("Please fill all required fields.", "danger")
            return redirect(url_for("auth.signup"))

        # Validate role
        if role not in ["student", "owner"]:
            flash("Invalid role selected.", "danger")
            return redirect(url_for("auth.signup"))

        # Check password confirmation
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("auth.signup"))

        # Password length
        if len(password) < 8:
            flash("Password must be at least 8 characters long.", "danger")
            return redirect(url_for("auth.signup"))

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already exists!", "danger")
            return redirect(url_for("auth.signup"))

        # Create user
        user = User(
            fullname=fullname,
            email=email,
            phone=phone,
            role=role
        )

        user.set_password(password)

        try:
            db.session.add(user)
            db.session.commit()

            flash("Registration Successful! Please Login.", "success")
            return redirect(url_for("auth.login"))

        except Exception:
            db.session.rollback()
            flash("Something went wrong. Please try again.", "danger")

    return render_template("auth/signup.html")


# ----------------------------
# Login
# ----------------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    # Already logged in
    if current_user.is_authenticated:
        return redirect(url_for("home.index"))

    if request.method == "POST":

        email = request.form.get("email").strip().lower()
        password = request.form.get("password")

        # Find user
        user = User.query.filter_by(email=email).first()

        # Verify credentials
        if user and user.check_password(password):

            login_user(user)

            flash("Login Successful!", "success")

            return redirect(url_for("home.index"))

        flash("Invalid email or password.", "danger")

    return render_template("auth/login.html")


# ----------------------------
# Logout
# ----------------------------
@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged out successfully.", "success")

    return redirect(url_for("home.index"))