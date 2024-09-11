import os
import sqlite3
from flask import Flask, g
from markupsafe import escape

app = Flask(__name__)
dbFile = "things.db"

def db():
    if 'db' not in g:
        dbPath = os.path.join(app.root_path, "data", dbFile)
        g.db = sqlite3.connect(dbPath, autocommit=True)  # Connect to the DB file
        g.db.row_factory = sqlite3.Row  # Want rows as dicts
    return g.db

@app.teardown_appcontext
def teardown_database(exception):
    dbCon = g.pop('db', None)
    if dbCon is not None:
        dbCon.close()

@app.get("/")
def helloWorld():
    query = """
        SELECT thing.id AS tid,
               thing.name AS tname,
               user.name AS uname 
        FROM thing
        JOIN user on thing.owner = user.id    
    """
    things = db().execute(query).fetchall()
    for thing in things:
        print(f"{thing['tid']}: {thing['tname']} ({thing['uname']})")
    return "<h1>Hello, World!</h1>"

@app.get("/hello/<name>")
def hello(name: str):
    query = """
        INSERT INTO thing (name, owner) VALUES ("Bacon", 1)    
    """
    db().execute(query)
    return f"<h1>Hello, {escape(name)}!</h1>"


