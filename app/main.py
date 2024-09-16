'''
MAIN APP ROUTES
'''


from flask import Blueprint
from flask import request
from flask import render_template
from flask import redirect
from flask import session
from flask import make_response

from .db import get_db
from .files import save_file, get_file, delete_file


main = Blueprint('main', __name__)


#-------------------------------------------------------
def login_required(func):
    '''
    Protect routes that require user to be logged in
    '''
    def secure_function():
        # Session info exists?
        if 'username' not in session:
            # No, so prompt to login
            return redirect('/login')
        return func()
    return secure_function


#-------------------------------------------------------
@main.get('/')

def hello():
    '''
    Home page
    '''
    name = 'Guest'
    if 'name' in session:
        name = session['name']

    return render_template(
        'pages/home.jinja',
        name=name
    )


#-------------------------------------------------------
@main.route("/profile")
@login_required

def profile():
    '''
    User profile page
    '''
    # Get the logged-in user's details
    db = get_db()
    query = 'SELECT * FROM users WHERE username=?'
    user = db.execute(query, (session['username'],)).fetchone()

    return render_template(
        'pages/profile.jinja',
        user=user
    )


#-------------------------------------------------------
@main.get('/things')

def list_things():
    '''
    Things page
    '''
    # Get thing details, including owner info
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
        'pages/things.jinja',
        things=things
    )


#-------------------------------------------------------
@main.post('/things/new')

def new_thing():
    '''
    New thing processing
    '''
    # Get form data
    name  = request.form['name']
    owner = request.form['owner']
    # And the uploaded image
    image = request.files['image']
    # Save the image, getting back the filename
    filename = save_file(image)
    # Add the item to the DB
    db = get_db()
    query = 'INSERT INTO things (name, owner, image) VALUES (?, ?, ?)'
    db.execute(query, (name, owner, filename))

    return redirect('/things')


#-------------------------------------------------------
@main.delete('/things/<id>')

def delete_thing(id:int):
    '''
    Delete a Thing
    '''
    # Get info about the thing to delete
    db = get_db()
    query = 'SELECT image, owner FROM things WHERE id=?'
    thing = db.execute(query, (id,)).fetchone()

    # Check that this belongs to the logged in user
    if session['id'] and thing['owner'] == session['id']:
        # Yep, so remove the associated file
        delete_file(thing['image'])
        # And delete the DB record
        query = 'DELETE FROM things WHERE id=?'
        db.execute(query, (id,))

        return make_response('', 200)   # Success

    else:
        # Should not be deleting
        return make_response('', 403)   # Forbidden


#-------------------------------------------------------
@main.get('/users')

def list_users():
    '''
    All users page
    '''
    db = get_db()
    query = 'SELECT * FROM users ORDER BY name ASC'
    users = db.execute(query).fetchall()

    return render_template(
        'pages/users.jinja',
        users=users
    )


#-------------------------------------------------------
@main.get('/users/<id>')

def show_user(id:int):
    '''
    Users page, but with specific user focused
    '''
    db = get_db()
    query = 'SELECT * FROM users ORDER BY name ASC'
    users = db.execute(query).fetchall()

    return render_template(
        'pages/users.jinja',
        users=users,
        focus_user=id
    )


#-------------------------------------------------------
@main.get('/users/<id>/details')

def user_details(id:int):
    '''
    User details component from HTMX request
    '''
    db = get_db()
    # Get user info
    query = 'SELECT * FROM users WHERE id=?'
    user = db.execute(query, (id,)).fetchone()
    # And list of owned things
    query = 'SELECT * FROM things WHERE owner=?'
    things = db.execute(query, (id,)).fetchall()

    return render_template(
        'components/user.jinja',
        user = user,
        things = things
    )


#-------------------------------------------------------
@main.delete('/users/<id>')

def delete_user(id:int):
    '''
    Delete a User
    '''
    # Check that this is the logged in user
    if session['id'] and int(id) == session['id']:
        # Delete the DB record
        db = get_db()
        query = 'DELETE FROM users WHERE id=?'
        db.execute(query, (id,))
        # Clear the session (login info)
        session.clear()
        # Return success (200)
        response = make_response('', 200)
        # Client redirect via HTMX to reload page
        response.headers['HX-Redirect'] = '/users'
        return response

    else:
        # Should not be deleting, forbidden (403)
        return make_response('', 403)


#-------------------------------------------------------
@main.get('/uploads/<filename>')

def uploaded_file(filename):
    '''
    Uploaded File Route (for thing images)
    '''
    return get_file(filename)


#-------------------------------------------------------
@main.errorhandler(404)

def not_found(e):
    '''
    Missing resource page
    '''
    return render_template('pages/404.jinja')



