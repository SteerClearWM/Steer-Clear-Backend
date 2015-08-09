
# db uri string for mysql db. form: 'mysql+mysqldb://username:password@server_address/db_name'
SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://steerclear:St33rCl3@r@localhost/db'
TEST_SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://steerclear:St33rCl3@r@localhost/test'

WTF_CSRF_ENABLED = False

SECRET_KEY = 'generate a secret key and place here'

TWILIO_ACCOUNT_SID = "Your Twilio Account SID Number Here"
TWILIO_AUTH_TOKEN = "Your Twilio Auth Token Here"
TWILIO_NUMBER = "Your Twilio Number Here"
