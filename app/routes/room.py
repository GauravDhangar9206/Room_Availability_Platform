import os
from werkzeug.utils import secure_filename

from app.models.image import Image



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
    
@room_bp.route("/edit/<int:room_id>", methods=["GET", "POST"])
@login_required
def edit_room(room_id):

    room = Room.query.get_or_404(room_id)

    # Only the owner can edit
    if room.owner_id != current_user.id:
        flash("You are not authorized to edit this room.", "danger")
        return redirect(url_for("home.index"))

    if request.method == "POST":

        room.title = request.form.get("title")
        room.description = request.form.get("description")
        room.room_type = request.form.get("room_type")
        room.rent = float(request.form.get("rent"))
        room.deposit = float(request.form.get("deposit") or 0)
        room.address = request.form.get("address")
        room.city = request.form.get("city")
        room.area = request.form.get("area")
        room.pincode = request.form.get("pincode")
        room.bedrooms = int(request.form.get("bedrooms"))
        room.bathrooms = int(request.form.get("bathrooms"))
        room.furnished = True if request.form.get("furnished") else False

        db.session.commit()

        flash("Room updated successfully!", "success")

        return redirect(url_for("room.room_detail", room_id=room.id))

    return render_template(
        "room/edit_room.html",
        room=room
    )

@room_bp.route("/delete/<int:room_id>", methods=["POST"])
@login_required
def delete_room(room_id):

    room = Room.query.get_or_404(room_id)

    if room.owner_id != current_user.id:
        flash("You are not authorized to delete this room.", "danger")
        return redirect(url_for("home.index"))

    db.session.delete(room)
    db.session.commit()

    flash("Room deleted successfully!", "success")

    return redirect(url_for("home.index"))
