from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('steerclear.settings.default_settings')
app.config.from_envvar('STEERCLEAR_SETTINGS')
db = SQLAlchemy(app)

from steerclear import views
from steerclear.views import api

app.register_blueprint(api)