from flask import Blueprint, flash, render_template, url_for, redirect
from flask.ext.login import login_user, logout_user, login_required, current_user
from flask_restful import abort
from sqlalchemy import exc
from steerclear import login_manager
from forms import *
from models import *

# setup login blueprint
login_bp = Blueprint('login', __name__)

"""
user_loader
-----------
Returns a user given the (unicode) user_id.
this needs to be implemented for flask-login extension to work
"""
@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

"""
login
-----
main endpoint for logging users in and out
GET - returns the login page
POST - logs user in if valid email and password
       and redirects to index page else returns the login template
:TODO: factor in password hashing + salt. add
       more helpful error messages
"""
@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('driver_portal.index'))
    return render_template('login.html', action=url_for('.login'))

"""
logout
------
Logs out the user. User must already be logged in, else
return 401. Once user is logged out, redirect to login page
"""
@login_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))

"""
register
--------
Main endpoint for registering new users in the system
GET - returns the register user template
POST - takes a email/password form and creates a new user.
       If a user already exists with the same email, flash an error message
       and return the register screen again. On success, redirect user to login page
"""
@login_bp.route('/register', methods=['GET', 'POST'])
def register():
    # attempt to validate UserForm
    form = UserForm()
    if form.validate_on_submit():
        # attempt to create a new User in the db
        new_user = User(
            email=form.email.data, 
            password=form.password.data,
            phone=form.phone.data
        )
        try:
            db.session.add(new_user)
            db.session.commit()
        except exc.IntegrityError:
            # user already exists
            return render_template('login.html', action=url_for('.register')), 409
        return redirect(url_for('.login'))
    return render_template('login.html', action=url_for('.register'))

@login_bp.route('/test_login')
@login_required
def test_login():
    return "Congrats, you are logged in as user " + str(current_user)
