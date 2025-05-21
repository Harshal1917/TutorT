# tutorT/app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap # Add this import
from config import Config
from flask import Blueprint

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login' # Will create an 'auth' blueprint with a 'login' route later
login.login_message_category = 'info' # For flash messages
bootstrap = Bootstrap() # Add this line

# tutorT/app/__init__.py
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app) # Add this line to initialize Bootstrap

    # Import and register the main blueprint
    # Import and register blueprints
    from app.main_routes import bp as main_bp # Assuming you have a main_bp
    app.register_blueprint(main_bp)

    # Import and register the admin blueprint
    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    # It's common to import models here as well, so Flask-Migrate can find them
    from app import models
    # Register other blueprints like auth here later
    # from app.auth.routes import bp as auth_bp
    # app.register_blueprint(auth_bp, url_prefix='/auth')

    # Context processor for datetime
    from datetime import datetime
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}

    # Custom Jinja2 filter for datetime formatting
    def datetimeformat(value, format='%Y'):
        return value.strftime(format)
    app.jinja_env.filters['datetimeformat'] = datetimeformat

    return app

from app import models # Keep this at the bottom