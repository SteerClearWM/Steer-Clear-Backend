from flask_wtf import Form
from wtforms import TextField, PasswordField, StringField
from wtforms.validators import DataRequired, Length, ValidationError
import phonenumbers as pn

"""
validate_phone
--------------
Custom validator. Validates that a StringField
that represents a phone number is in the correct format
"""
def validate_phone(form, field):
    try:
        # parse field into PhoneNumber object
        phone = pn.parse(field.data, None)

        # if StringField is not in the correct format, raise validation error
        if not pn.is_valid_number(phone) or not pn.is_possible_number(phone):
            raise ValidationError('Field must be valid phone number')
    except pn.phonenumberutil.NumberParseException:
        raise ValidationError('Field must be valid phone number')

"""
RegisterForm
------------
Form for validating registration requests.
Has email, password, and phone number fields
for the new user
"""
class RegisterForm(Form):
    email = TextField('email', [DataRequired(), Length(min=1, max=119)])
    password = PasswordField('password', [DataRequired(), Length(min=1, max=119)])
    phone = StringField('phone', [DataRequired(), validate_phone])

"""
LoginForm
---------
Form for validating login requests.
Has email and password fields for the
user that is attempting to login
"""
class LoginForm(Form):
    email = TextField('email', [DataRequired(), Length(min=1, max=119)])
    password = PasswordField('password', [DataRequired(), Length(min=1, max=119)])