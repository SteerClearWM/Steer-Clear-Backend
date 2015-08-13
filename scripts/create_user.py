import sys, os

# change path to parent directory to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from steerclear import db
from steerclear.models import User, Role
from sqlalchemy import exc

def create_user():
	# prompt for input
	email = raw_input('Enter email: ')
	phone = raw_input('Enter Phone Number (e.x. +1xxxyyyzzzz): ')
	role = None
	while role not in ['student', 'admin']:
		role = raw_input('Enter Role (student | admin): ')
	
	role = Role.query.filter_by(name=role).first()
	if role is None:
		print "Error: Role does not exist. Start app once and make request"
		sys.exit(1)

	# create user
	user = User(email=email, phone=phone, roles=[role])
	try:
		# attempt to add user to db
		db.session.add(user)
		db.session.commit()
		print "User created successfully"
	except exc.IntegrityError:
		print "User already exists"

if __name__ == '__main__':
	create_user()