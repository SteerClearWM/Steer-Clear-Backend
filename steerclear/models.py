# from flask.ext.sqlalchemy import SQLAlchemy
from steerclear import db
import sqlalchemy.types as types

"""
Model class for the Ride object
"""
class Ride(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20))
    num_passengers = db.Column(db.Integer)
    start_lat = db.Column(db.Float)
    start_long = db.Column(db.Float)
    end_lat = db.Column(db.Float)
    end_long = db.Column(db.Float)

    def __init__(self, phone_number, num_passengers, pickup, dropoff):
        self.phone_number = phone_number
        self.num_passengers = num_passengers
        self.start_lat, self.start_long = pickup
        self.end_lat, self.end_long = dropoff

    def __repr__(self):
        return "<Ride(Phone %r, Passengers %r, Pickup <%r, %r>, Dropoff <%r, %r>)>" % \
                (self.phone_number, self.num_passengers, self.start_lat, self.start_long,
                 self.end_lat, self.end_long)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

