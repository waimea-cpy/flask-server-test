import os
import sqlite3
from flask import Flask, g
from markupsafe import escape


#=======================================================================
# APP SETUP

app = Flask(__name__)


#=======================================================================
# ROUTES

#-------------------------------------------
# Home Page
@app.get("/")
def helloWorld():
    query = """
        SELECT  thing.id   AS tid,
                thing.name AS tname,
                user.name  AS uname 
        FROM thing
        JOIN user ON thing.owner = user.id    
    """
    things = db().execute(query).fetchall()
    for thing in things:
        print(f"{thing['tid']}: {thing['tname']} ({thing['uname']})")
    return "<h1>Hello, World!</h1>"


#-------------------------------------------
# Greeting
@app.get("/hello/<name>")
def hello(name: str):
    query = """
        INSERT INTO thing (name, owner) VALUES ("Bacon", 1)    
    """
    db().execute(query)
    return f"<h1>Hello, {escape(name)}!</h1>"



#=======================================================================
# DATABASE

#-------------------------------------------
# Retrieve / create DB connection
def db():
    if 'db' not in g:
        dbPath = os.path.join(app.root_path, "data/data.db")
        g.db = sqlite3.connect(dbPath, autocommit=True)  # Connect to the DB file
        g.db.row_factory = sqlite3.Row  # Want rows as dicts
    return g.db

#-------------------------------------------
# Disconnect when app run is complete
@app.teardown_appcontext
def teardown_database(exception):
    dbCon = g.pop('db', None)
    if dbCon is not None:
        dbCon.close()


#=======================================================================
# LAUNCH if run as script

if __name__ == "__main__":
    app.run()

