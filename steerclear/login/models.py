from steerclear import db
from flask.ext import login
from sqlalchemy_utils.types.phone_number import PhoneNumberType

class User(db.Model, login.UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(120))
    phone_number = db.Column(PhoneNumberType, unique=True)

    def __repr__(self):
        return "User(ID %r, Email %r, Password %r, Phone %r)" % (
            self.id,
            self.email,
            self.password,
            self.phone_number.e164
        )
