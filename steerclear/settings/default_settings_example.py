
# db uri string for mysql db. form: 'mysql+mysqldb://username:password@server_address/db_name'
SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://steerclear:St33rCl3@r@localhost/db'
TEST_SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://steerclear:St33rCl3@r@localhost/test'

WTF_CSRF_ENABLED = False

# secrete key 
SECRET_KEY = 'generate a secret key and place here'

# twilio account info
TWILIO_ACCOUNT_SID = "Your Twilio Account SID Number Here"
TWILIO_AUTH_TOKEN = "Your Twilio Auth Token Here"
TWILIO_NUMBER = "Your Twilio Number Here"

# a valid wm account username and password for running tests
TEST_CAS_USERNAME = 'your-username'
TEST_CAS_PASSWORD = 'your-password'

# path to file you wish to send logs to
LOGGING_FILENAME = 'path_to_your_logfile.log'

# mysql times out idle connections after a certain amount of time
# set this to the amount of time db connections can remain
# idle before being refreshed
# SQLALCHEMY_POOL_RECYCLE = 'idle_time_limit_in_seconds'
