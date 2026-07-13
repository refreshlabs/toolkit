import os

from flask import Flask, render_template

from config import BASE_DIR, Config
from app.extensions import db
from app.routes import register_blueprints


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    os.makedirs(os.path.join(BASE_DIR, "instance"), exist_ok=True)

    db.init_app(app)
    register_blueprints(app)

    from app.cli import register_cli
    register_cli(app)

    @app.context_processor
    def inject_nav():
        return {"org_name": "Refresh Labs"}

    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    return app
