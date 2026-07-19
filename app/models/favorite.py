from datetime import datetime

from app.extensions import db


class Favorite(db.Model):

    __tablename__ = "favorites"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

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

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    student = db.relationship(
        "User",
        backref="favorites"
    )

    room = db.relationship(
        "Room",
        backref="favorites"
    )