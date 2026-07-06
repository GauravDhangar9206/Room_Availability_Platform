from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash

from .extension import db
from .modules import User

main = Blueprint("main", __name__)


# -------------------- Home --------------------

@main.route("/")
def home():
    return render_template("home/index.html")


@main.route("/about")
def about():
    return render_template("home/about.html")


@main.route("/contact")
def contact():
    return render_template("home/contact.html")


# -------------------- Login --------------------

@main.route("/login")
def login():
    return render_template("auth/login.html")


# -------------------- Signup --------------------

@main.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        role = request.form["role"]

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already exists!")
            return redirect(url_for("main.signup"))

        # Hash password
        hashed_password = generate_password_hash(password)

        # Create user object
        new_user = User(
            name=name,
            email=email,
            phone=phone,
            password=hashed_password,
            role=role
        )

        # Save to database
        db.session.add(new_user)
        db.session.commit()

        flash("Registration Successful!")

        return redirect(url_for("main.login"))

    return render_template("auth/signup.html")


# -------------------- Role Selection --------------------

@main.route("/select-role")
def select_role():
    return render_template("auth/select_role.html")