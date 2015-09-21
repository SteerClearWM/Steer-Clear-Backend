import sys, os

# change path to parent directory to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from steerclear.models import User, Role
from steerclear import db

def main():
	username = raw_input('Enter username of user you would like to make admin: ')

	user = User.query.filter_by(username=username).first()
	if user is None:
		print "Error: user <%s> does not exist" % username
		sys.exit(0)

	admin_role = Role.query.filter_by(name='admin').first()
	if admin_role is None:
		print "Error: Role does not exist. Start app once and make request"
		sys.exit(0)

	# if they aren't already an admin, make them an admin
	if admin_role not in user.roles:
		user.roles.append(admin_role)
		db.session.commit()
		print "%s is now an admin" % username
	else:
		print "%s is already an admin" % username



if __name__ == '__main__':
	main()










