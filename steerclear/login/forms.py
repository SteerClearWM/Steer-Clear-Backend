from flask_wtf import Form
from wtforms import TextField, PasswordField, StringField
from wtforms.validators import DataRequired, Length

def validate_phone(form, field):
	pass

class UserForm(Form):
	email = TextField('email', [DataRequired(), Length(min=1, max=119)])
	password = PasswordField('password', [DataRequired(), Length(min=1, max=119)])
	phone = StringField('phone', [DataRequired(), validate_phone])
