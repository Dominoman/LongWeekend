from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()


def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from . import commands as command_module
    command_module.register(app)

    with app.app_context():
        from . import models
        return app