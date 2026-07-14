from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db
from app.models.room import Room

room_bp = Blueprint("room", __name__, url_prefix="/rooms")


@room_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_room():

    # Only owners can add rooms
    if current_user.role != "owner":
        flash("Only Room Owners can add rooms.", "danger")
        return redirect(url_for("home.index"))

    if request.method == "POST":

        title = request.form.get("title")
        description = request.form.get("description")
        room_type = request.form.get("room_type")
        rent = request.form.get("rent")
        deposit = request.form.get("deposit")
        address = request.form.get("address")
        city = request.form.get("city")
        area = request.form.get("area")
        pincode = request.form.get("pincode")
        bedrooms = request.form.get("bedrooms")
        bathrooms = request.form.get("bathrooms")

        furnished = True if request.form.get("furnished") else False

        room = Room(
            title=title,
            description=description,
            room_type=room_type,
            rent=float(rent),
            deposit=float(deposit) if deposit else 0,
            address=address,
            city=city,
            area=area,
            pincode=pincode,
            bedrooms=int(bedrooms),
            bathrooms=int(bathrooms),
            furnished=furnished,
            owner=current_user
        )

        db.session.add(room)
        db.session.commit()

        flash("Room added successfully!", "success")

        return redirect(url_for("home.index"))

    return render_template("room/create_room.html")