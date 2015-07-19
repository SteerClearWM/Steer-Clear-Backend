from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class UserForm(Form):
	username = StringField('username', [DataRequired(), Length(max=119)])
	password = StringField('password', [DataRequired(), Length(max=119)])
