import pprint
from flask import Blueprint
from flask import current_app
from flask import request
from flask import render_template
from flask import redirect
from flask import session
from flask import send_from_directory
from flask import make_response

from .db import get_db
from .files import save_file, delete_file


#=======================================================================
# MAIN ROUTES

main = Blueprint('main', __name__)


#-------------------------------------------
# Protect routes that require user to be logged in
def login_required(func):
    def secure_function():
        if 'username' not in session:
            return redirect('/login')
        return func()
    return secure_function


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
# User Profile
@main.route("/profile")
@login_required

def profile():
    db = get_db()
    query = 'SELECT * FROM users WHERE username=?'
    user = db.execute(query, (session['username'],)).fetchone()

    return render_template('profile.jinja', user=user)


#-------------------------------------------
# Things Page
@main.get('/things')

def list_things():
    db = get_db()
    query = '''
        SELECT  things.id    AS t_id,
                things.name  AS t_name,
                things.image AS t_image,
                users.id     AS u_id,
                users.name   AS u_name
        FROM things
        JOIN users ON things.owner = users.id
        ORDER BY things.name ASC
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
        INSERT INTO things (name, owner, image)
        VALUES (?, ?, ?)
    '''
    db.execute(query, (name, owner, filename))

    return redirect('/things')


#-------------------------------------------
# Delete a Thing
@main.delete('/things/<id>')

def delete_thing(id:int):
    db = get_db()
    query = 'SELECT image, owner FROM things WHERE id=?'
    thing = db.execute(query, (id,)).fetchone()

    # Check that this belongs to the logged in user
    if session['id'] and thing['owner'] == session['id']:
        delete_file(thing['image'])
        query = 'DELETE FROM things WHERE id=?'
        db.execute(query, (id,))
        return make_response('', 200)   # Success

    else:
        return make_response('', 403)   # Forbidden


#-------------------------------------------
# Users Page
@main.get('/users')

def list_users():
    db = get_db()
    query = 'SELECT * FROM users ORDER BY name ASC'
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
    query = 'SELECT * FROM users ORDER BY name ASC'
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
    query = 'SELECT * FROM users WHERE id=?'
    user = db.execute(query, (id,)).fetchone()
    query = 'SELECT * FROM things WHERE owner=?'
    things = db.execute(query, (id,)).fetchall()

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



