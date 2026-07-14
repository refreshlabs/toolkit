import os
import warnings

from flask import Flask, render_template, session
from markupsafe import Markup, escape

from config import BASE_DIR, Config
from app.extensions import db
from app.routes import register_blueprints
from app.services.content import get_content


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    if app.config["ADMIN_PASSWORD"] == "changeme-refreshlabs":
        warnings.warn(
            "ADMIN_PASSWORD is using the insecure default. "
            "Set the ADMIN_PASSWORD environment variable before deploying.",
            stacklevel=2,
        )

    os.makedirs(os.path.join(BASE_DIR, "instance"), exist_ok=True)

    db.init_app(app)
    register_blueprints(app)

    from app.cli import register_cli
    register_cli(app)

    @app.context_processor
    def inject_nav():
        return {
            "org_name": "Refresh Labs",
            "is_admin": session.get("is_admin", False),
            "csrf_token": session.get("csrf_token", ""),
        }

    @app.template_global()
    def editable(key, default):
        value = get_content(key, default)
        if session.get("is_admin"):
            return Markup(
                f'<span class="admin-editable" data-editable-key="{escape(key)}">{escape(value)}</span>'
            )
        return Markup(escape(value))

    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    return app
