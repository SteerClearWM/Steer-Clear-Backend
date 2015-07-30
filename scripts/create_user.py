import sys, os

# change path to parent directory to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from steerclear import db
from steerclear.models import User
from sqlalchemy import exc

def create_user():
	# prompt for input
	email = raw_input('Enter Email: ')
	password = raw_input('Enter Password: ')
	
	# create user
	user = User(email=email, password=password)
	try:
		# attempt to add user to db
		db.session.add(user)
		db.session.commit()
		print "User created successfully"
	except exc.IntegrityError:
		print "User already exists"

if __name__ == '__main__':
	create_user()