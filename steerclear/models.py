# from flask.ext.sqlalchemy import SQLAlchemy
from steerclear import db
import sqlalchemy.types as types
from datetime import datetime

"""
Model class for the Ride object
"""
class Ride(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num_passengers = db.Column(db.Integer)
    start_latitude = db.Column(db.Float)
    start_longitude = db.Column(db.Float)
    end_latitude = db.Column(db.Float)
    end_longitude = db.Column(db.Float)

    def __init__(self, num_passengers, pickup, dropoff, pickup_time, travel_time, dropoff_time):
        self.num_passengers = num_passengers
        self.start_latitude, self.start_longitude = pickup
        self.end_latitude, self.end_longitude = dropoff

    def __repr__(self):
        return "<Ride(ID %r, Passengers %r, Pickup <%r, %r>, Dropoff <%r, %r>, ETA %r)>" % \
                (
                    self.id,
                    self.num_passengers, 
                    self.start_latitude, 
                    self.start_longitude,
                    self.end_latitude, 
                    self.end_longitude,
                )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

