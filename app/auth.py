from flask import Blueprint
from flask import current_app
from flask import request
from flask import render_template
from flask import redirect
from flask import session
from flask import flash

from flask_bcrypt import Bcrypt

from .db import get_db


#=======================================================================
# AUTH ROUTES

auth = Blueprint('auth', __name__)


#-------------------------------------------
# Sign Up Page
@auth.get('/signup')

def sign_up_form():
    return render_template('signup.jinja')


#-------------------------------------------
# Sign Up Processing
@auth.post('/signup')

def add_user():
    name     = request.form['name']
    username = request.form['username']
    password = request.form['password']

    db = get_db()
    query = 'SELECT * FROM user WHERE username=?'
    user = db.execute(query, (username,)).fetchone()

    if user:
        flash(f'Existing account with username: <strong>{username}</strong>', 'error')
        return redirect('/signup')

    else:
        query = '''
            INSERT INTO user (name, username, hash)
            VALUES (?, ?, ?)
        '''

        bcrypt = Bcrypt(current_app)
        hash = bcrypt.generate_password_hash(password).decode('utf-8')

        db.execute(query, (name, username, hash))

        flash('Account created. Please login')
        return redirect('/login')


#-------------------------------------------
# Login Page
@auth.get('/login')

def login_form():
    return render_template('login.jinja')


#-------------------------------------------
# Login Processing
@auth.post('/login')

def login_user():
    username = request.form['username']
    password = request.form['password']

    db = get_db()
    query = 'SELECT * FROM user WHERE username=?'
    user = db.execute(query, (username,)).fetchone()

    if user:
        bcrypt = Bcrypt(current_app)

        if bcrypt.check_password_hash(user['hash'], password):
            session['id']       = user['id']
            session['username'] = user['username']
            session['name']     = user['name']
            return redirect('/')

        else:
            flash('Incorrect password', 'error')
            return redirect('/login')

    else:
        flash(f'Unknown username: <strong>{username}</strong>', 'error')
        return redirect('/login')



#-------------------------------------------
# Logout Processing
@auth.get('/logout')

def logout_user():
    session.clear()
    return redirect('/')


