from flask import Blueprint, flash
from flask.ext.login import login_user
from forms import *
from models import *

login_bp = Blueprint('login', __name__, url_prefix='/login')

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    form = UserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            login_user(user)
            return "logged in"
    return "not logged in"
