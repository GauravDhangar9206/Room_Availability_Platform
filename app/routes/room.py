from flask import Blueprint

room_bp = Blueprint("room", __name__, url_prefix="/rooms")


@room_bp.route("/")
def index():
    return "Room Blueprint Working!"