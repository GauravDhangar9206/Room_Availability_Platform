from flask import Blueprint, render_template

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("home/index.html")


@main.route("/about")
def about():
    return render_template("home/about.html")


@main.route("/contact")
def contact():
    return render_template("home/contact.html")


@main.route("/login")
def login():
    return render_template("auth/login.html")


@main.route("/signup")
def signup():
    return render_template("auth/signup.html")


@main.route("/select-role")
def select_role():
    return render_template("auth/select_role.html")