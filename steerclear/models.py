# from flask.ext.sqlalchemy import SQLAlchemy
from steerclear import db

"""
Model class for the Ride object
"""
class Ride(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    phone_number = db.Column(db.String(20))

    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number

    def __repr__(self):
        return "<Ride(Name %r, Number %r)>" % (self.name, self.phone_number)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
