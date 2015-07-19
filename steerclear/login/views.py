from flask import Blueprint, flash, render_template, url_for, redirect
from flask.ext.login import login_user, login_required
from steerclear import login_manager
from forms import *
from models import *


login_bp = Blueprint('login', __name__, url_prefix='/login')

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    form = UserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('driver_portal.index'))
    return render_template('login.html')

@login_bp.route('/test')
@login_required
def test():
	return "Congrats, you are logged in"
