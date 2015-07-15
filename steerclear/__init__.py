from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('steerclear.settings.default_settings')
app.config.from_envvar('STEERCLEAR_SETTINGS')
db = SQLAlchemy(app)

from steerclear import views
from steerclear.api.views import api
from steerclear.driver_portal.views import driver_portal

app.register_blueprint(api)
app.register_blueprint(driver_portal)
