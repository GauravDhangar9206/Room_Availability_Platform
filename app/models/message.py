from datetime import datetime

from app.extensions import db


class Message(db.Model):

    __tablename__ = "messages"

    # ==========================================
    # PRIMARY KEY
    # ==========================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # ==========================================
    # SENDER
    # ==========================================

    sender_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # ==========================================
    # RECEIVER
    # ==========================================

    receiver_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # ==========================================
    # ROOM
    # ==========================================

    room_id = db.Column(
        db.Integer,
        db.ForeignKey("rooms.id"),
        nullable=False
    )

    # ==========================================
    # MESSAGE TEXT
    # ==========================================

    message = db.Column(
        db.Text,
        nullable=False
    )

    # ==========================================
    # CREATED TIME
    # ==========================================

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # ==========================================
    # SENDER RELATIONSHIP
    # ==========================================

    sender = db.relationship(
        "User",
        foreign_keys=[sender_id],
        backref="sent_messages"
    )

    # ==========================================
    # RECEIVER RELATIONSHIP
    # ==========================================

    receiver = db.relationship(
        "User",
        foreign_keys=[receiver_id],
        backref="received_messages"
    )

    # ==========================================
    # ROOM RELATIONSHIP
    # ==========================================

    room = db.relationship(
        "Room",
        backref="messages"
    )