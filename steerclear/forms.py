# from flask_wtf import Form
# from wtforms import IntegerField, StringField, FloatField
# from wtforms.validators import DataRequired, NumberRange, Length
# from models import Ride

# """
# RideForm
# --------
# Form validator for creating a new ride object.
# Should validate that all form parameters are required
# and are of the right type, length, etc...
# """
# class RideForm(Form):
#     num_passengers = IntegerField('num_passengers', [DataRequired(), NumberRange(min=1, max=8)])
#     start_latitude = FloatField('start_latitude', [DataRequired()])
#     start_longitude = FloatField('start_longitude', [DataRequired()])
#     end_latitude = FloatField('end_latitude', [DataRequired()])
#     end_longitude = FloatField('end_longitude', [DataRequired()])
