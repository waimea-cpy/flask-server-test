'''
SQLITE DATABASE RELATED FUNCTIONS
- Connecting
- Initialising
- Closing
'''

import os
import sqlite3
import click
from flask import current_app, g


#-------------------------------------------------------
def get_db():
    '''
    Retrieve / create DB connection
    '''
    # Are we already connected to the DB?
    if 'db' not in g:
        # Connect to the DB file and save connection in flask global store
        database_path = os.path.join(
            current_app.root_path, 'data',
            current_app.config['DB_FILE']
        )
        g.db = sqlite3.connect(database_path, autocommit=True)
        g.db.row_factory = sqlite3.Row  # Want rows as dicts

    # Pass back the connection
    return g.db


#-------------------------------------------------------
def init_db():
    '''
    Recreate the DB from the given schema.sql
    '''
    db = get_db()
    # Open and read the schema file
    schema_path = os.path.join('data', current_app.config['DB_SCHEMA'])
    with current_app.open_resource(schema_path) as f:
        # Execute the SQL commands within
        db.executescript(f.read().decode('utf8'))


#-------------------------------------------------------
def close_db(e=None):
    '''
    Close any open DB connection
    '''
    # Get the saved connection from the global store
    db = g.pop('db', None)
    if db is not None:
        db.close()


#-------------------------------------------------------
def init_app(app):
    '''
    Register 'flask init-db' command and
    define the teardown action when app completes
    '''
    # Register the init command
    app.cli.add_command(init_db_command)
    # Define the teardown process for the DB
    app.teardown_appcontext(close_db)


#-------------------------------------------------------
# Respond to the 'flask init-db' command
@click.command('init-db')

def init_db_command():
    '''
    Clear the DB and re-initialise the schema.
    '''
    init_db()
    click.echo('DB cleared and initialised')

