from flask import Blueprint, render_template

from app.models.room import Room

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def index():

    rooms = Room.query.filter_by(available=True).all()

    return render_template(
        "home/index.html",
        rooms=rooms
    )