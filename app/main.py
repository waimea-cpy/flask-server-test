from flask import Blueprint
from flask import request
from flask import render_template
from flask import redirect
from flask import session

from .db import get_db


#=======================================================================
# MAIN ROUTES

main = Blueprint('main', __name__)


#-------------------------------------------
# Home Page
@main.get("/")

def hello():
    name = "Guest"
    if session.get('name'):
        name = session['name']

    return render_template(
        "home.jinja",
        name = name
    )


#-------------------------------------------
# Things Page
@main.get("/things")

def list_things():
    db = get_db()
    query = """
        SELECT  thing.id   AS t_id,
                thing.name AS t_name,
                user.name  AS u_name
        FROM thing
        JOIN user ON thing.owner = user.id
        ORDER BY thing.name ASC
    """
    things = db.execute(query).fetchall()

    return render_template(
        "things.jinja",
        things = things
    )


#-------------------------------------------
# New Thing
@main.post("/thing/new")

def new_thing():
    name = request.form['name']
    owner = request.form['owner']

    db = get_db()
    query = """
        INSERT INTO thing (name, owner)
        VALUES (?, ?)
    """

    db.execute(query, (name, owner))

    return redirect("/things")


#-------------------------------------------
# Users Page
@main.get("/users")

def list_users():
    db = get_db()
    query = "SELECT * FROM user ORDER BY name ASC"
    users = db.execute(query).fetchall()

    return render_template(
        "users.jinja",
        users = users
    )


#-------------------------------------------
# Users Page
@main.get("/user/<id>")

def show_user(id:int):
    db = get_db()

    query = "SELECT * FROM user WHERE id=?"
    user = db.execute(query, (id,)).fetchone()

    query = "SELECT * FROM thing WHERE owner=?"
    things = db.execute(query, (id,)).fetchall()

    return render_template(
        "user.jinja",
        user = user,
        things = things
    )



#-------------------------------------------
# Missing Pages
@main.errorhandler(404)

def not_found(e):
    return render_template("404.jinja")



