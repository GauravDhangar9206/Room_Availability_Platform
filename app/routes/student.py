from flask import Blueprint, render_template
from flask_login import login_required, current_user

student_bp = Blueprint(
    "student",
    __name__,
    url_prefix="/student"
)


@student_bp.route("/dashboard")
@login_required
def dashboard():

    if current_user.role != "student":
        return "Access Denied", 403

    return render_template("student/dashboard.html")