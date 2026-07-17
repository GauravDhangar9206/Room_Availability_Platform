from datetime import datetime

from app.extensions import db


class Booking(db.Model):

    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    room_id = db.Column(
        db.Integer,
        db.ForeignKey("rooms.id"),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Pending"
    )

    booking_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    student = db.relationship(
        "User",
        backref="bookings"
    )

    room = db.relationship(
        "Room",
        backref="bookings"
    )