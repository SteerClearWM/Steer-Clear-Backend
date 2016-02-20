from steerclear import db
from flask.ext import login
from sqlalchemy_utils.types.phone_number import PhoneNumberType
from sqlalchemy_utils import force_auto_coercion

# This is needed so that if we create a User object
# by passing it a string as a phone number, it will
# coerce the string to a phone number object
force_auto_coercion()

association_table = db.Table('association_table',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    
    users = db.relationship('User', secondary=association_table, backref='roles', lazy='dynamic')

    def __repr__(self):
        return "Role(Name %r)" % (
                self.name,
            )

class User(db.Model, login.UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    phone = db.Column(PhoneNumberType, unique=True)

    rides = db.relationship('Ride', backref='user', lazy='dynamic')

    def __repr__(self):
        return "User(ID %r, Username %r, Roles %r)" % (
            self.id,
            self.username,
            self.roles.all()
        )
