import os
from flask import Flask


#=======================================================================
# APP SETUP

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = 'THIS IS MY SECRET KEY'
    app.config['DATABASE'] = os.path.join(app.root_path, 'data/data.db')
    app.config['UPLOADS']  = os.path.join(app.root_path, 'uploads')

    # Routing blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Setup DB and Files handlers
    from . import db
    db.init_app(app)
    from . import files
    files.init_app(app)

    return app


