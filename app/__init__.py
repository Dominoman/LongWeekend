import logging
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()

def configure_console_logging(app, level=logging.INFO):
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))

    # attach to Flask app logger
    app.logger.setLevel(level)
    app.logger.addHandler(handler)
    app.logger.propagate = False

    # also send Werkzeug (request) logs to console
    werkzeug_logger = logging.getLogger("werkzeug")
    werkzeug_logger.setLevel(level)
    werkzeug_logger.addHandler(handler)

def punctuation(value):
    return '{:,.0f}'.format(value).replace(',', '.')

def to_time(value):
    """Convert a number of seconds to a formatted time string."""
    value = int(value)
    hours, remainder = divmod(value, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}"

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.jinja_env.filters['punctuation'] = punctuation
    app.jinja_env.filters['to_time'] = to_time

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from . import commands as command_module
    command_module.register(app)
    configure_console_logging(app)

    with app.app_context():
        from . import models
        return app