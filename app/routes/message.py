from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from app.models.room import Room
from app.models.message import Message
from app.models.user import User


message_bp = Blueprint(
    "message",
    __name__,
    url_prefix="/message"
)


# ==========================================
# CHAT PAGE
# ==========================================

@message_bp.route("/chat/<int:room_id>")
@login_required
def chat(room_id):

    # ------------------------------------------
    # GET ROOM
    # ------------------------------------------

    room = Room.query.get_or_404(room_id)


    # ------------------------------------------
    # ONLY STUDENT CAN START CHAT
    # ------------------------------------------

    if current_user.role != "student":

        flash(
            "Only students can chat with room owners.",
            "danger"
        )

        return redirect(
            url_for(
                "room.room_detail",
                room_id=room.id
            )
        )


    # ------------------------------------------
    # GET ROOM OWNER
    # ------------------------------------------

    other_user = User.query.get_or_404(
        room.owner_id
    )


    # ------------------------------------------
    # GET ALL MESSAGES
    # ------------------------------------------

    messages = Message.query.filter(

        (

            (Message.sender_id == current_user.id)

            &

            (Message.receiver_id == other_user.id)

        )

        |

        (

            (Message.sender_id == other_user.id)

            &

            (Message.receiver_id == current_user.id)

        )

    ).order_by(

        Message.created_at.asc()

    ).all()


    # ------------------------------------------
    # SEND DATA TO CHAT.HTML
    # ------------------------------------------

    return render_template(

        "message/chat.html",

        room=room,

        other_user=other_user,

        messages=messages

    )