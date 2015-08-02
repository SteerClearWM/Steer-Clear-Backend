from flask_wtf import Form
from wtforms import TextField, PasswordField, StringField
from wtforms.validators import DataRequired, Length, ValidationError
import phonenumbers as pn

def validate_phone(form, field):
    try:
        phone = pn.parse(field.data, None)
        if not pn.is_valid_number(phone) or not pn.is_possible_number(phone):
            raise ValidationError('Field must be valid phone number')
    except pn.phonenumberutil.NumberParseException:
        raise ValidationError('Field must be valid phone number')

class RegisterForm(Form):
    email = TextField('email', [DataRequired(), Length(min=1, max=119)])
    password = PasswordField('password', [DataRequired(), Length(min=1, max=119)])
    phone = StringField('phone', [DataRequired(), validate_phone])


class LoginForm(Form):
    email = TextField('email', [DataRequired(), Length(min=1, max=119)])
    password = PasswordField('password', [DataRequired(), Length(min=1, max=119)])