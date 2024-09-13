import os
import sqlite3

from flask import Flask
from flask import g
from flask import render_template
from flask import redirect
from flask import request
from flask import session

from flask_bcrypt import Bcrypt


#=======================================================================
# APP SETUP

app = Flask(__name__)

app.config["SECRET_KEY"] = "THIS IS MY SECRET KEY"
bcrypt = Bcrypt(app)


#=======================================================================
# ROUTES

#-------------------------------------------
# Home Page
@app.get("/")

def hello():
    name = "Guest"
    if session.get('name'):
        name = session['name']

    return render_template(
        "home.jinja",
        name = name
    )


#-------------------------------------------
# Sign Up Page
@app.get("/signup")

def sign_up_form():
    return render_template("signup.jinja")


#-------------------------------------------
# Sign Up Processing
@app.post("/signup")

def add_user():
    name     = request.form['name']
    username = request.form['username']
    password = request.form['password']

    query = "SELECT * FROM user WHERE username=?"
    user = db().execute(query, (username,)).fetchone()

    if user:
        return render_template(
            "info.jinja",
            info = f"Account with username '{username}' already exists!"
        )

    else:
        query = """
            INSERT INTO user (name, username, hash)
            VALUES (?, ?, ?)
        """

        hash = bcrypt.generate_password_hash(password).decode('utf-8')

        db().execute(query, (name, username, hash))

        return redirect("/login")


#-------------------------------------------
# Login Page
@app.get("/login")

def login_form():
    return render_template("login.jinja")


#-------------------------------------------
# Login Processing
@app.post("/login")

def login_user():
    username = request.form['username']
    password = request.form['password']

    query = "SELECT * FROM user WHERE username=?"
    user = db().execute(query, (username,)).fetchone()

    if user:
        if bcrypt.check_password_hash(user['hash'], password):
            session['id']       = user['id']
            session['username'] = user['username']
            session['name']     = user['name']
            return redirect("/")

        else:
            return render_template(
                "info.jinja",
                info = f"Incorrect password"
            )

    else:
        return render_template(
            "info.jinja",
            info = f"Unknown user '{username}'"
        )


#-------------------------------------------
# Logout Processing
@app.get("/logout")

def logout_user():
    session.clear()
    return redirect("/")


#-------------------------------------------
# Things Page
@app.get("/things")

def list_things():
    query = """
        SELECT  thing.id   AS t_id,
                thing.name AS t_name,
                user.name  AS u_name
        FROM thing
        JOIN user ON thing.owner = user.id
        ORDER BY thing.name ASC
    """
    things = db().execute(query).fetchall()

    return render_template(
        "things.jinja",
        things = things
    )


#-------------------------------------------
# New Thing
@app.post("/thing/new")

def new_thing():
    query = """
        INSERT INTO thing (name, owner)
        VALUES (?, ?)
    """
    name = request.form['name']
    owner = request.form['owner']

    db().execute(query, (name, owner))

    return redirect("/things")


#-------------------------------------------
# Users Page
@app.get("/users")

def list_users():
    query = "SELECT * FROM user ORDER BY name ASC"
    users = db().execute(query).fetchall()

    return render_template(
        "users.jinja",
        users = users
    )


#-------------------------------------------
# Users Page
@app.get("/user/<id>")

def show_user(id:int):
    query = "SELECT * FROM user WHERE id=?"
    user = db().execute(query, (id,)).fetchone()

    query = "SELECT * FROM thing WHERE owner=?"
    things = db().execute(query, (id,)).fetchall()

    return render_template(
        "user.jinja",
        user = user,
        things = things
    )



#-------------------------------------------
# Missing Pages
@app.errorhandler(404)

def not_found(e):
    return render_template("404.jinja")



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

