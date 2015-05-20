from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('steerclear.settings.default_settings')
db = SQLAlchemy(app)

from steerclear import views
