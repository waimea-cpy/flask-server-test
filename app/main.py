import pprint
from flask import Blueprint
from flask import current_app
from flask import request
from flask import render_template
from flask import redirect
from flask import session
from flask import send_from_directory

from .db import get_db
from .files import save_file


#=======================================================================
# MAIN ROUTES

main = Blueprint('main', __name__)


#-------------------------------------------
# Home Page
@main.get('/')

def hello():
    name = 'Guest'
    if 'name' in session:
        name = session['name']

    return render_template(
        'home.jinja',
        name = name
    )


#-------------------------------------------
# Things Page
@main.get('/things')

def list_things():
    db = get_db()
    query = '''
        SELECT  thing.id    AS t_id,
                thing.name  AS t_name,
                thing.image AS t_image,
                user.name   AS u_name
        FROM thing
        JOIN user ON thing.owner = user.id
        ORDER BY thing.name ASC
    '''
    things = db.execute(query).fetchall()

    return render_template(
        'things.jinja',
        things = things
    )


#-------------------------------------------
# New Thing
@main.post('/things/new')

def new_thing():
    name  = request.form['name']
    owner = request.form['owner']
    image = request.files['image']
    filename = save_file(image)

    db = get_db()
    query = '''
        INSERT INTO thing (name, owner, image)
        VALUES (?, ?, ?)
    '''
    db.execute(query, (name, owner, filename))

    return redirect('/things')


#-------------------------------------------
# Users Page
@main.get('/users')

def list_users():
    db = get_db()
    query = 'SELECT * FROM user ORDER BY name ASC'
    users = db.execute(query).fetchall()

    return render_template(
        'users.jinja',
        users = users
    )


#-------------------------------------------
# Users Page
@main.get('/users/<id>')

def show_user(id:int):
    db = get_db()
    query = 'SELECT * FROM user ORDER BY name ASC'
    users = db.execute(query).fetchall()

    return render_template(
        'users.jinja',
        users = users,
        user_id = id
    )


#-------------------------------------------
# Users Page
@main.get('/users/<id>/details')

def user_details(id:int):
    db = get_db()
    query = 'SELECT * FROM user WHERE id=?'
    user = db.execute(query, (id,)).fetchone()
    query = 'SELECT * FROM thing WHERE owner=?'
    things = db.execute(query, (id,)).fetchall()

    htmx = 'HX-Request' in request.headers

    return render_template(
        'components/user.jinja',
        user = user,
        things = things
    )


#-------------------------------------------
# Uploaded File Route (for images)
@main.get('/uploads/<filename>')

def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOADS'], filename)


#-------------------------------------------
# Missing Pages
@main.errorhandler(404)

def not_found(e):
    return render_template('404.jinja')



