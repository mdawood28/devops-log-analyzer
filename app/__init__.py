import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from config import config_map

db = SQLAlchemy()
csrf = CSRFProtect()


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config_map[config_name])

    db.init_app(app)
    csrf.init_app(app)

    _setup_logging(app)
    _register_blueprints(app)

    with app.app_context():
        db.create_all()

    return app


def _setup_logging(app):
    if app.config.get("TESTING"):
        return

    log_file = app.config.get("LOG_FILE", "logs/app.log")
    log_dir = os.path.dirname(log_file)
    os.makedirs(log_dir, exist_ok=True)

    handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=5)
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)


def _register_blueprints(app):
    from app.routes.main import main_bp
    from app.routes.logs import logs_bp
    from app.routes.errors import errors_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(logs_bp, url_prefix="/logs")
    app.register_blueprint(errors_bp)
