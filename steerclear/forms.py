from flask_wtf import Form
from wtforms import IntegerField, StringField, FloatField
from wtforms.validators import DataRequired, NumberRange, Length
from models import Ride

"""
RideForm
--------
Form validator for creating a new ride object.
Should validate that all form parameters are required
and are of the right type, length, etc...
"""
class RideForm(Form):
    phone_number = StringField('phone_number', [DataRequired(), Length(min=8, max=20)])
    num_passengers = IntegerField('num_passengers', [DataRequired(), NumberRange(min=1, max=8)])
    start_latitude = FloatField('start_latitude', [DataRequired()])
    start_longitude = FloatField('start_longitude', [DataRequired()])
    end_latitude = FloatField('end_latitude', [DataRequired()])
    end_longitude = FloatField('end_longitude', [DataRequired()])

    """
    as_ride
    -------
    convert the current form object to a Ride object
    """
    def as_ride(self):
        return Ride(
            self.phone_number.data,
            self.num_passengers.data,
            (self.start_latitude.data, self.start_longitude.data),
            (self.end_latitude.data, self.end_longitude.data)
        )