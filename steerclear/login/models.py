from steerclear import db
from flask.ext import login
from sqlalchemy_utils.types.phone_number import PhoneNumberType
from sqlalchemy_utils import force_auto_coercion

# This is needed so that if we create a User object
# by passing it a string as a phone number, it will
# coerce the string to a phone number object
force_auto_coercion()

class User(db.Model, login.UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(120))
    phone = db.Column(PhoneNumberType, unique=True)

    rides = db.relationship('Ride', backref='user', lazy='dynamic')

    def __repr__(self):
        return "User(ID %r, Email %r, Password %r, Phone %r)" % (
            self.id,
            self.email,
            self.password,
            self.phone
        )
