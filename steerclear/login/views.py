from flask import (
    Blueprint, 
    render_template, 
    url_for, 
    redirect, 
    current_app,
    session,
    request
)
from flask.ext.login import (
    login_user, 
    logout_user, 
    login_required, 
    current_user
)
from flask.ext.principal import (
    Principal,
    Identity, 
    AnonymousIdentity, 
    identity_changed, 
    identity_loaded, 
    Permission,
    RoleNeed, 
    UserNeed
)
from flask_restful import abort
from sqlalchemy import exc
from steerclear import login_manager, app 
from steerclear.utils import cas
from steerclear.utils.permissions import (
    admin_permission, 
    student_permission,
    AccessRideNeed
)
from forms import *
from models import *

# setup login blueprint
login_bp = Blueprint('login', __name__)

# setup flask-principal
principal = Principal()
principal.init_app(app)

"""
create_roles
------------
Function called before app processes first request.
Creates the admin and student Roles if they do
not already exist
"""
@app.before_first_request
def create_roles():
    # create student Role
    if Role.query.filter_by(name='student').first() is None:
        role = Role(name='student', description='Student Role')
        db.session.add(role)
        db.session.commit()
    # create admin Role
    if Role.query.filter_by(name='admin').first() is None:
        role = Role(name='admin', description='Admin Role')
        db.session.add(role)
        db.session.commit()

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
identity_loaded
---------------
Signal used by flask-principal. called when
loading the user Identity for the request. 
"""
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.name))

    # Assuming the User model has a list of rides the user
    # has requested, add the needs to the identity
    if hasattr(current_user, 'rides'):
        for ride in current_user.rides:
            identity.provides.add(AccessRideNeed(unicode(ride.id)))

"""
login
-----
main endpoint for logging users in and out
GET - returns the login page
POST - logs user in if valid username and password
       and redirects to index page else returns the login template
:TODO: factor in password hashing + salt. add
       more helpful error messages
"""
@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    # GET request. return login page
    if request.method == 'GET':
        return render_template('login.html', action=url_for('.login'))

    # POST request. attempt to login
    # must validate LoginForm and CAS server
    form = LoginForm()
    if form.validate_on_submit() and cas.validate_user(form.username.data, form.password.data):
        
        # get User object if exists
        user = User.query.filter_by(username=form.username.data).first()
        if user:

            # login user
            login_user(user)

            # Tell Flask-Principal the identity changed
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id))

            return redirect(url_for('driver_portal.index'))
    return render_template('login.html', action=url_for('.login')), 400

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

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())

    return redirect(url_for('.login'))

"""
register
--------
Main endpoint for registering new users in the system
POST - takes a username/password form and creates a new user.
       If a user already exists with the same username, flash an error message
       and return the register screen again. On success, redirect user to login page
"""
@login_bp.route('/register', methods=['POST'])
def register():
    # POST request. attempt to validate RegisterForm and user with CAS server
    form = RegisterForm()
    if form.validate_on_submit() and cas.validate_user(form.username.data, form.password.data):
        
        # Find StudentRole. SHOULD EXIST ON STARTUP. IF NOT, THEN SERVER ERROR
        student_role = Role.query.filter_by(name='student').first()
        if student_role is None:
            abort(500)

        # attempt to create a new User in the db
        new_user = User(
            username=form.username.data, 
            phone=form.phone.data,
            roles=[student_role]
        )
        try:
            db.session.add(new_user)
            db.session.commit()
        except exc.IntegrityError:
            # user already exists
            return render_template('login.html', action=url_for('.register')), 409
        return redirect(url_for('.login'))
    return render_template('login.html', action=url_for('.register')), 400
