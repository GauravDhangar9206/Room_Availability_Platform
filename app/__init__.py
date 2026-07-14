from flask import Flask

from app.config import Config
from app.extensions import db, migrate, login_manager
from app.models.user import User

from app.routes.home import home_bp
from app.routes.auth import auth_bp


def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register Blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)

    # Flask-Login user loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app