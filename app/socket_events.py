from flask_socketio import (
    join_room,
    emit
)

from flask_login import current_user

from app.extensions import db
from app.models.message import Message


def register_socket_events(socketio):


    # ==========================================
    # JOIN CHAT ROOM
    # ==========================================

    @socketio.on("join")
    def handle_join(data):

        # Get chat room name
        chat_room = data.get("room")


        # Check room
        if not chat_room:

            return


        # Join Socket.IO room
        join_room(chat_room)


        print(
            f"User joined chat room: {chat_room}"
        )


    # ==========================================
    # SEND MESSAGE
    # ==========================================

    @socketio.on("send_message")
    def handle_send_message(data):

        # --------------------------------------
        # GET DATA
        # --------------------------------------

        chat_room = data.get(
            "room"
        )

        message_text = data.get(
            "message"
        )

        sender_id = data.get(
            "sender_id"
        )

        receiver_id = data.get(
            "receiver_id"
        )

        room_id = data.get(
            "room_id"
        )


        # --------------------------------------
        # VALIDATE DATA
        # --------------------------------------

        if not message_text:

            return


        if not sender_id:

            return


        if not receiver_id:

            return


        if not room_id:

            return


        if not chat_room:

            return


        # --------------------------------------
        # CREATE MESSAGE
        # --------------------------------------

        new_message = Message(

            sender_id=int(
                sender_id
            ),

            receiver_id=int(
                receiver_id
            ),

            room_id=int(
                room_id
            ),

            message=message_text.strip()

        )


        # --------------------------------------
        # SAVE MESSAGE
        # --------------------------------------

        db.session.add(
            new_message
        )

        db.session.commit()


        # --------------------------------------
        # MESSAGE DATA
        # --------------------------------------

        message_data = {

            "id":
                new_message.id,

            "message":
                new_message.message,

            "sender_id":
                new_message.sender_id,

            "receiver_id":
                new_message.receiver_id,

            "room_id":
                new_message.room_id,

            "created_at":
                new_message.created_at.strftime(
                    "%I:%M %p"
                )

        }


        # --------------------------------------
        # SEND TO CHAT ROOM
        # --------------------------------------

        emit(

            "receive_message",

            message_data,

            to=chat_room

        )


        print(
            "Message saved successfully:",
            message_data
        )