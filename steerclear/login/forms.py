from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Length

class UserForm(Form):
	email = TextField('email', [DataRequired(), Length(min=1, max=119)])
	password = PasswordField('password', [DataRequired(), Length(min=1, max=119)])
