from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

#initialize flask app with correct configurations
app = Flask(__name__)
app.config.from_object('steerclear.settings.default_settings')
app.config.from_envvar('STEERCLEAR_SETTINGS')
db = SQLAlchemy(app)

from steerclear import views
from steerclear.api.views import api
from steerclear.driver_portal.views import driver_portal

# register all blueprints to the app
app.register_blueprint(api)
app.register_blueprint(driver_portal)
