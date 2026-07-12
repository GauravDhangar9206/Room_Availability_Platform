from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Database object
db = SQLAlchemy()

# Migration object
migrate = Migrate()

# Login manager
login_manager = LoginManager()

# Redirect users to login page if authentication is required
login_manager.login_view = "auth.login"

# Flash message category
login_manager.login_message_category = "info"