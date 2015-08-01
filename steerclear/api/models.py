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
    pickup_time = db.Column(types.DateTime)
    travel_time = db.Column(db.Integer)
    dropoff_time = db.Column(types.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "<Ride(ID %r, Passengers %r, Pickup <%r, %r>, Dropoff <%r, %r>, ETP %r, Duration %r, ETD %r)>" % \
                (
                    self.id,
                    self.num_passengers, 
                    self.start_latitude, 
                    self.start_longitude,
                    self.end_latitude, 
                    self.end_longitude,
                    self.pickup_time,
                    self.travel_time,
                    self.dropoff_time,
                )

    def as_dict(self):
        return {
            'id': self.id,
            'num_passengers': self.num_passengers,
            'start_latitude': self.start_latitude,
            'start_longitude': self.start_longitude,
            'end_latitude': self.end_latitude,
            'end_longitude': self.end_longitude,
            'pickup_time': self.pickup_time,
            'travel_time': self.travel_time,
            'dropoff_time': self.dropoff_time,
        }
