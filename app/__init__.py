import os
from flask import Flask


#=======================================================================
# APP SETUP

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config["SECRET_KEY"] = "THIS IS MY SECRET KEY"
    app.config["DATABASE"] = os.path.join(app.root_path, "data/data.db")

    # Routing blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Setup DB
    from . import db
    db.init_app(app)

    return app

