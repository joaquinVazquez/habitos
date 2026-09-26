from flask import Flask

from config import config_by_name
from app.extensions import db, migrate


def create_app(config_name="production"):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.habitos import habitos_bp
    app.register_blueprint(habitos_bp)

    from app import models 

    return app
