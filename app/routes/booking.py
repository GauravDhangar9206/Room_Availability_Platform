from flask import Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db
from app.models.booking import Booking
from app.models.room import Room

booking_bp = Blueprint(
    "booking",
    __name__,
    url_prefix="/booking"
)


@booking_bp.route("/book/<int:room_id>")
@login_required
def book_room(room_id):

    if current_user.role != "student":
        flash("Only students can book rooms.", "danger")
        return redirect(url_for("home.index"))

    room = Room.query.get_or_404(room_id)

    existing_booking = Booking.query.filter_by(
        student_id=current_user.id,
        room_id=room.id
    ).first()

    if existing_booking:
        flash("You have already requested this room.", "warning")
        return redirect(url_for("room.room_detail", room_id=room.id))

    booking = Booking(
        student=current_user,
        room=room
    )

    db.session.add(booking)
    db.session.commit()

    flash("Booking request sent successfully.", "success")

    return redirect(url_for("room.room_detail", room_id=room.id))