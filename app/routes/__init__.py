def register_blueprints(app):
    from app.routes.main import main_bp
    from app.routes.learn import learn_bp
    from app.routes.laboratory import laboratory_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(learn_bp)
    app.register_blueprint(laboratory_bp)
    app.register_blueprint(admin_bp)
