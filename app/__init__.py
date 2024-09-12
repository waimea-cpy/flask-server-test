import os
import sqlite3
from flask import Flask, g, render_template, redirect, request
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
    return render_template(
        "greet.jinja",
        title = "Hello, World!"
    )


#-------------------------------------------
# Greeting
@app.get("/hello/<name>")

def hello(name:str):
    return render_template(
        "greet.jinja",
        title = "Hello, Human!",
        name = name
    )


#-------------------------------------------
# Things Page
@app.get("/things")

def listThings():
    query = """
        SELECT  thing.id   AS t_id,
                thing.name AS t_name,
                user.name  AS u_name
        FROM thing
        JOIN user ON thing.owner = user.id
    """
    thingRecords = db().execute(query).fetchall()

    query = "SELECT * FROM user ORDER BY name ASC"
    peopleRecords = db().execute(query).fetchall()

    return render_template(
        "things.jinja",
        title = "All the Things",
        things = thingRecords,
        people = peopleRecords
    )


#-------------------------------------------
# New Thing
@app.post("/thing/new")

def newThing():
    query = """
        INSERT INTO thing (name, owner)
        VALUES (?, ?)
    """
    name = request.form['name']
    owner = request.form['owner']

    db().execute(query, (name, owner))

    return redirect("/things")


#-------------------------------------------
# People Page
@app.get("/people")

def listPeople():
    query = "SELECT * FROM user ORDER BY name ASC"
    peopleRecords = db().execute(query).fetchall()

    return render_template(
        "people.jinja",
        title = "All the People",
        people = peopleRecords
    )


#-------------------------------------------
# People Page
@app.get("/person/<id>")

def showPerson(id:int):
    query = "SELECT * FROM user WHERE id=?"
    personRecord = db().execute(query, (id,)).fetchone()

    query = "SELECT * FROM thing WHERE owner=?"
    thingRecords = db().execute(query, (id,)).fetchall()

    return render_template(
        "person.jinja",
        title = "Person Details",
        person = personRecord,
        things = thingRecords
    )


#-------------------------------------------
# New Person
@app.post("/person/new")

def newPerson():
    query = """
        INSERT INTO user (name)
        VALUES (?)
    """
    name = request.form['name']

    db().execute(query, (name,))

    return redirect("/people")



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

