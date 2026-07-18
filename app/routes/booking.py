from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import login_required, current_user

from app.extensions import db
from app.models.booking import Booking
from app.models.room import Room

booking_bp = Blueprint(
    "booking",
    __name__,
    url_prefix="/booking"
)


# ----------------------------------
# Book a Room
# ----------------------------------
@booking_bp.route("/book/<int:room_id>")
@login_required
def book_room(room_id):

    if current_user.role != "student":
        flash("Only students can book rooms.", "danger")
        return redirect(url_for("home.index"))

    room = Room.query.get_or_404(room_id)

    booking = Booking.query.filter_by(
        student_id=current_user.id,
        room_id=room.id
    ).first()

    if booking:
        flash("You have already booked this room.", "warning")
        return redirect(url_for("room.room_detail", room_id=room.id))

    booking = Booking(
        student_id=current_user.id,
        room_id=room.id,
        status="Pending"
    )

    db.session.add(booking)
    db.session.commit()

    flash("Room booked successfully.", "success")

    return redirect(url_for("booking.my_bookings"))


# ----------------------------------
# Student My Bookings
# ----------------------------------
@booking_bp.route("/my-bookings")
@login_required
def my_bookings():

    if current_user.role != "student":
        flash("Access Denied.", "danger")
        return redirect(url_for("home.index"))

    bookings = Booking.query.filter_by(
        student_id=current_user.id
    ).all()

    return render_template(
        "booking/my_bookings.html",
        bookings=bookings
    )
    
# ----------------------------------
# Owner Booking Requests
# ----------------------------------
@booking_bp.route("/requests")
@login_required
def owner_bookings():

    if current_user.role != "owner":
        flash("Access Denied.", "danger")
        return redirect(url_for("home.index"))

    bookings = Booking.query.join(Room).filter(
        Room.owner_id == current_user.id
    ).all()

    return render_template(
        "booking/booking_requests.html",
        bookings=bookings
    )


# ----------------------------------
# Approve Booking
# ----------------------------------
@booking_bp.route("/approve/<int:booking_id>")
@login_required
def approve_booking(booking_id):

    if current_user.role != "owner":
        flash("Access Denied.", "danger")
        return redirect(url_for("home.index"))

    booking = Booking.query.get_or_404(booking_id)

    if booking.room.owner_id != current_user.id:
        flash("Unauthorized.", "danger")
        return redirect(url_for("home.index"))

    booking.status = "Approved"

    db.session.commit()

    flash("Booking Approved Successfully.", "success")
    return redirect(url_for("booking.owner_bookings"))


# ----------------------------------
# Reject Booking
# ----------------------------------
@booking_bp.route("/reject/<int:booking_id>")
@login_required
def reject_booking(booking_id):

    if current_user.role != "owner":
        flash("Access Denied.", "danger")
        return redirect(url_for("home.index"))

    booking = Booking.query.get_or_404(booking_id)

    if booking.room.owner_id != current_user.id:
        flash("Unauthorized.", "danger")
        return redirect(url_for("home.index"))

    booking.status = "Rejected"

    db.session.commit()

    flash("Booking Rejected.", "warning")

    return redirect(url_for("booking.owner_bookings"))