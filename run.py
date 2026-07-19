from app import create_app
from flask_socketio import SocketIO

from app.socket_events import register_socket_events


# Create Flask application
app = create_app()


# Create SocketIO application
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="threading"
)


# Register SocketIO events
register_socket_events(socketio)


if __name__ == "__main__":

    socketio.run(
        app,
        debug=True,
        allow_unsafe_werkzeug=True
    )