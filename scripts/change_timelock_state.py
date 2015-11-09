import sys, os

# change path to parent directory to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from steerclear import db
from steerclear.models import TimeLock
from sqlalchemy import exc

def main():
	# prompt for input
	new_state = raw_input('Enter New TimeLock State(on/off): ')
	
	if new_state not in ['on', 'off']:
		print 'Error: invalid state input selection'
		sys.exit(1)

	timelock = TimeLock.query.first()
	if timelock is None:
		print "Error: TimeLock not initialized. make request to api to create timelock"
		sys.exit(1)
	
	if new_state == 'on':
		timelock.state = True
	else:
		timelock.state = False
	db.session.commit()
	print 'Timelocks state changed to %s' % new_state


if __name__ == '__main__':
    main()
