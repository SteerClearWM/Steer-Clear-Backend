from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Length

class UserForm(Form):
	username = TextField('username', [DataRequired(), Length(min=1, max=119)])
	password = PasswordField('password', [DataRequired(), Length(min=1, max=119)])
