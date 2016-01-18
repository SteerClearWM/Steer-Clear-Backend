from steerclear import db
import sqlalchemy.types as types
from datetime import datetime

"""
Model class for the Ride object
"""
class Ride(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.now())
    num_passengers = db.Column(db.Integer, nullable=False)
    
    start_latitude = db.Column(db.Float, nullable=False)
    start_longitude = db.Column(db.Float, nullable=False)
    
    end_latitude = db.Column(db.Float, nullable=False)
    end_longitude = db.Column(db.Float, nullable=False)
    
    pickup_time = db.Column(types.DateTime, nullable=False)
    travel_time = db.Column(db.Integer, nullable=False)
    dropoff_time = db.Column(types.DateTime, nullable=False)

    pickup_address = db.Column(db.String(255), nullable=False)
    dropoff_address = db.Column(db.String(255), nullable=False)

    on_campus = db.Column(db.Boolean, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

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
            'pickup_address': self.pickup_address,
            'dropoff_address': self.dropoff_address,
            'on_campus': self.on_campus
        }
