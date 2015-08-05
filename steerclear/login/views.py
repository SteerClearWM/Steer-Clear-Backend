from flask import (
    Blueprint, 
    render_template, 
    url_for, 
    redirect, 
    current_app,
    session
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
from forms import *
from models import *

# setup login blueprint
login_bp = Blueprint('login', __name__)

# setup flask-principal
principal = Principal()
principal.init_app(app)

# Create 2 permissions. 1 for admins and 1 for students
admin_permission = Permission(RoleNeed('admin'))
student_permission = Permission(RoleNeed('student'))

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

            # Tell Flask-Principal the identity changed
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id))

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
GET - returns the register user template
POST - takes a email/password form and creates a new user.
       If a user already exists with the same email, flash an error message
       and return the register screen again. On success, redirect user to login page
"""
@login_bp.route('/register', methods=['GET', 'POST'])
def register():
    # attempt to validate RegisterForm
    form = RegisterForm()
    if form.validate_on_submit():
        
        # Find StudentRole. SHOULD EXIST ON STARTUP. IF NOT, THEN SERVER ERROR
        student_role = Role.query.filter_by(name='student').first()
        if student_role is None:
            abort(500)

        # attempt to create a new User in the db
        new_user = User(
            email=form.email.data, 
            password=form.password.data,
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
    return render_template('login.html', action=url_for('.register'))

@login_bp.route('/test_student_permission')
@login_required
@student_permission.require(http_exception=403)
def test_student_permission():
    return "Congrats, you are a student"

@login_bp.route('/test_login')
@login_required
def test_login():
    return "Congrats, you are logged in as user " + str(current_user)
