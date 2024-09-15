'''
APP CONFIGURATION AND SETUP
'''

from flask import Flask


def create_app():
    '''
    Setup the app with appropriate configuration
    and initialise other modules as needed
    '''

    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY']  = 'THIS IS MY SECRET KEY'
    app.config['DB_FILE']     = 'data.db'
    app.config['DB_SCHEMA']   = 'schema.sql'
    app.config['UPLOADS_DIR'] = 'uploads'

    # Prevent cookies being retained after browser close
    app.config["SESSION_PERMANENT"] = False

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


