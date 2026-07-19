from flask import Flask

from app.config import Config
from app.extensions import db, migrate, login_manager

# Models
from app.models.user import User
from app.models.room import Room
from app.models.booking import Booking
from app.models.favorite import Favorite
from app.models.message import Message

# Blueprints
from app.routes.home import home_bp
from app.routes.auth import auth_bp
from app.routes.room import room_bp
from app.routes.search import search_bp
from app.routes.booking import booking_bp
from app.routes.favorite import favorite_bp
from app.routes.message import message_bp



def create_app():

    app = Flask(__name__)

    # Load Configuration
    app.config.from_object(Config)

    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    # Register Blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(room_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(favorite_bp)
    app.register_blueprint(message_bp)

    # Flask Login User Loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app