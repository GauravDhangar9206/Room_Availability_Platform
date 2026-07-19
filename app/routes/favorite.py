from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import login_required, current_user

from app.extensions import db
from app.models.favorite import Favorite
from app.models.room import Room

favorite_bp = Blueprint(
    "favorite",
    __name__,
    url_prefix="/favorite"
)


# -----------------------------
# Add to Favorites
# -----------------------------
@favorite_bp.route("/add/<int:room_id>")
@login_required
def add_favorite(room_id):

    if current_user.role != "student":
        flash("Only students can add favorites.", "danger")
        return redirect(url_for("home.index"))

    room = Room.query.get_or_404(room_id)

    favorite = Favorite.query.filter_by(
        student_id=current_user.id,
        room_id=room.id
    ).first()

    if favorite:
        flash("Room is already in your favorites.", "warning")
        return redirect(url_for("room.room_detail", room_id=room.id))

    favorite = Favorite(
        student_id=current_user.id,
        room_id=room.id
    )

    db.session.add(favorite)
    db.session.commit()

    flash("Room added to favorites.", "success")

    return redirect(url_for("room.room_detail", room_id=room.id))


# -----------------------------
# Remove Favorite
# -----------------------------
@favorite_bp.route("/remove/<int:room_id>")
@login_required
def remove_favorite(room_id):

    favorite = Favorite.query.filter_by(
        student_id=current_user.id,
        room_id=room_id
    ).first()

    if favorite:

        db.session.delete(favorite)
        db.session.commit()

        flash("Removed from favorites.", "success")

    return redirect(url_for("favorite.my_favorites"))


# -----------------------------
# My Favorites
# -----------------------------
@favorite_bp.route("/my-favorites")
@login_required
def my_favorites():

    if current_user.role != "student":
        flash("Access Denied.", "danger")
        return redirect(url_for("home.index"))

    favorites = Favorite.query.filter_by(
        student_id=current_user.id
    ).all()

    return render_template(
        "favorite/my_favorites.html",
        favorites=favorites
    )