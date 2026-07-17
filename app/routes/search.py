from flask import Blueprint, render_template, request
from sqlalchemy import or_

from app.models.room import Room

search_bp = Blueprint("search", __name__, url_prefix="/search")


@search_bp.route("/", methods=["GET"])
def search():

    keyword = request.args.get("keyword", "").strip()

    query = Room.query.filter(Room.available == True)

    if keyword:
        query = query.filter(
            or_(
                Room.title.ilike(f"%{keyword}%"),
                Room.city.ilike(f"%{keyword}%"),
                Room.area.ilike(f"%{keyword}%"),
                Room.room_type.ilike(f"%{keyword}%")
            )
        )

    rooms = query.all()

    return render_template(
        "search/search_results.html",
        rooms=rooms,
        keyword=keyword
    )