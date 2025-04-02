import os
from flask import Flask
from backend.extensions import mongo, bcrypt, login_manager, csrf  
from config.config import config  # ✅ Import config

def create_app():
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    app = Flask(
        __name__,
        template_folder=os.path.join(root_path, "templates"),
        static_folder=os.path.join(root_path, "static")
    )

    # ✅ Load configurations from config.py
    app.config.from_object(config)

    # ✅ Initialize extensions (Removed db & Migrate)
    mongo.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)  

    # ✅ Register Blueprints
    from backend.routes import routes_bp  
    app.register_blueprint(routes_bp, url_prefix="/")

    return app
