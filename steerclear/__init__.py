from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

#initialize flask app with correct configurations
app = Flask(__name__)
app.config.from_object('steerclear.settings.default_settings')
app.config.from_envvar('STEERCLEAR_SETTINGS')
db = SQLAlchemy(app)

from steerclear import views
from steerclear.api.views import api_bp
from steerclear.driver_portal.views import driver_portal
from steerclear.login.views import login_bp

# register all blueprints to the app
app.register_blueprint(api_bp)
app.register_blueprint(driver_portal)
app.register_blueprint(login_bp)

from flask.ext.login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
