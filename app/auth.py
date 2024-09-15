'''
AUTHORISATION-RELATED ROUTES
'''


from flask import Blueprint
from flask import current_app
from flask import request
from flask import render_template
from flask import redirect
from flask import session
from flask import flash

from flask_bcrypt import Bcrypt

from .db import get_db


auth = Blueprint('auth', __name__)


#-------------------------------------------------------
@auth.get('/signup')

def sign_up_form():
    '''
    Sign-up page
    '''
    return render_template('pages/signup.jinja')


#-------------------------------------------------------
@auth.post('/signup')

def add_user():
    '''
    Sign-up processing
    '''
    # Get data from form
    name     = request.form['name']
    username = request.form['username']
    password = request.form['password']

    # See if user already exists
    db = get_db()
    query = 'SELECT * FROM users WHERE username=?'
    user = db.execute(query, (username,)).fetchone()

    if user:
        # Yes, so alert them
        flash(f'Existing account with username: <strong>{username}</strong>', 'error')
        return redirect('/signup')

    else:
        # No, so hash the password and add the user to the DB
        bcrypt = Bcrypt(current_app)
        hash = bcrypt.generate_password_hash(password).decode('utf-8')
        query = 'INSERT INTO users (name, username, hash) VALUES (?, ?, ?)'
        db.execute(query, (name, username, hash))

        flash('Account created. Please login')
        return redirect('/login')


#-------------------------------------------------------
@auth.get('/login')

def login_form():
    '''
    Login page
    '''
    return render_template('pages/login.jinja')


#-------------------------------------------------------
@auth.post('/login')

def login_user():
    '''
    Login Processing
    '''
    # Get data from the form
    username = request.form['username']
    password = request.form['password']
    # Try to access the user's record
    db = get_db()
    query = 'SELECT * FROM users WHERE username=? COLLATE NOCASE'
    user = db.execute(query, (username,)).fetchone()

    if user:
        # User exists, so check the password hash
        if Bcrypt(current_app).check_password_hash(user['hash'], password):
            # Hashes match, so save the login into the session
            session['id']       = user['id']
            session['username'] = user['username']
            session['name']     = user['name']
            return redirect('/')

        else:
            # Hashes don't match
            flash('Incorrect password', 'error')
            return redirect('/login')

    else:
        # No user account found
        flash(f'Unknown username: <strong>{username}</strong>', 'error')
        return redirect('/login')



#-------------------------------------------------------
@auth.get('/logout')

def logout_user():
    '''
    Logout Processing
    '''
    # Clear the current session, and back to home page
    session.clear()
    return redirect('/')


