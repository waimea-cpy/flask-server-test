import sqlite3
import click
from flask import current_app, g


#-------------------------------------------
# Retrieve / create DB connection
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"], autocommit=True)  # Connect to the DB file
        g.db.row_factory = sqlite3.Row  # Want rows as dicts
    return g.db


#-------------------------------------------
# Recreate the DB from the given schema.sql
def init_db():
    db = get_db()
    with current_app.open_resource("data/schema.sql") as f:
        db.executescript(f.read().decode('utf8'))


#-------------------------------------------
# Close any open DB connection
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


#-------------------------------------------
# Register 'flask init-db' command and
# teardown action when app completes
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


#-------------------------------------------
# Respond to the 'flask init-db' command
@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('DB cleared and initialised')

