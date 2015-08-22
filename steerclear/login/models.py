from steerclear import db
from flask.ext import login
from sqlalchemy_utils.types.phone_number import PhoneNumberType
from sqlalchemy_utils import force_auto_coercion

# This is needed so that if we create a User object
# by passing it a string as a phone number, it will
# coerce the string to a phone number object
force_auto_coercion()

class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "Role(ID %r, Name %r, Description %r" % (
                self.id,
                self.name,
                self.description
            )

class User(db.Model, login.UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(PhoneNumberType, unique=True)

    rides = db.relationship('Ride', backref='user', lazy='dynamic')
    roles = db.relationship('Role', backref='user', lazy='dynamic')

    def __repr__(self):
        return "User(ID %r, Username %r, Phone %r)" % (
            self.id,
            self.username,
            self.phone
        )
