from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db
from app.models.room import Room

room_bp = Blueprint("room", __name__, url_prefix="/rooms")


@room_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_room():

    if current_user.role != "owner":
        flash("Only Room Owners can add rooms.", "danger")
        return redirect(url_for("home.index"))

    if request.method == "POST":

        room = Room(
            title=request.form.get("title"),
            description=request.form.get("description"),
            room_type=request.form.get("room_type"),
            rent=float(request.form.get("rent")),
            deposit=float(request.form.get("deposit") or 0),
            address=request.form.get("address"),
            city=request.form.get("city"),
            area=request.form.get("area"),
            pincode=request.form.get("pincode"),
            bedrooms=int(request.form.get("bedrooms")),
            bathrooms=int(request.form.get("bathrooms")),
            furnished=True if request.form.get("furnished") else False,
            owner=current_user
        )

        db.session.add(room)
        db.session.commit()

        flash("Room Added Successfully!", "success")

        return redirect(url_for("home.index"))

    return render_template("room/create_room.html")
@room_bp.route("/<int:room_id>")
def room_detail(room_id):

    room = Room.query.get_or_404(room_id)

    return render_template(
        "room/room_detail.html",
        room=room
    )