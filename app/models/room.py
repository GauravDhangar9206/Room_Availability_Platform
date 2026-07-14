from datetime import datetime

from app.extensions import db


class Room(db.Model):

    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)

    description = db.Column(db.Text, nullable=False)

    room_type = db.Column(db.String(50), nullable=False)

    rent = db.Column(db.Float, nullable=False)

    deposit = db.Column(db.Float, default=0)

    address = db.Column(db.String(255), nullable=False)

    city = db.Column(db.String(100), nullable=False)

    area = db.Column(db.String(100), nullable=False)

    pincode = db.Column(db.String(10), nullable=False)

    bedrooms = db.Column(db.Integer, default=1)

    bathrooms = db.Column(db.Integer, default=1)

    furnished = db.Column(db.Boolean, default=False)

    available = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    owner = db.relationship(
        "User",
        back_populates="rooms"
    )

    def __repr__(self):
        return f"<Room {self.title}>"