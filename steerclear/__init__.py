from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

#initialize flask app with correct configurations
app = Flask(__name__)
try:
	app.config.from_object('steerclear.settings.default_settings')
except ImportError as e:
	print e
	app.config.from_object('steerclear.settings.default_settings_example')
db = SQLAlchemy(app)

# setup login manager for flask-login
from flask.ext.login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

# setup sms client for twilio api
from steerclear.utils import sms
sms_client = sms.SteerClearSMSClient(
            app.config['TWILIO_ACCOUNT_SID'], 
            app.config['TWILIO_AUTH_TOKEN'],
            app.config['TWILIO_NUMBER']
        )

# setup google distance matrix api client
from steerclear.utils.eta import SteerClearDMClient
dm_client = SteerClearDMClient()

# setup and load in shapefile of the campus map
from steerclear.utils.polygon import SteerClearGISClient
gis_client = SteerClearGISClient(app.config['CAMPUS_MAP_SHAPEFILE'])

from steerclear.api.views import api_bp
from steerclear.driver_portal.views import driver_portal_bp
from steerclear.login.views import login_bp

# register all blueprints to the app
app.register_blueprint(api_bp)
app.register_blueprint(driver_portal_bp)
app.register_blueprint(login_bp)
