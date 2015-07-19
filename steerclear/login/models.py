from steerclear import db
from flask.ext import login
from steerclear import login_manager

class User(db.Model, login.UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(120))

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))