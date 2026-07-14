from datetime import datetime

from app.extensions import db


class Image(db.Model):

    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)

    filename = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    room_id = db.Column(
        db.Integer,
        db.ForeignKey("rooms.id"),
        nullable=False
    )

    room = db.relationship(
        "Room",
        back_populates="images"
    )

    def __repr__(self):
        return f"<Image {self.filename}>"