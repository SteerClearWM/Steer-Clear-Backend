from flask import Blueprint, flash
from flask.ext.login import *
from .forms import *

login_bp = Blueprint('login', __name__, url_prefix='/login')

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    form = UserForm()
    if form.validate_on_submit():
        login_user(user)
        return "logged in"
    return "not logged in"
