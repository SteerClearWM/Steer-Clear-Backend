import sys, os

# change path to parent directory to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from steerclear import db
from steerclear.models import Ride, User
from sqlalchemy import exc
from datetime import datetime

def create_user():
    # create user
    dt = datetime(1,1,1)
    ride = Ride(
            num_passengers=1,
            start_latitude=1.0,
            start_longitude=1.1,
            end_latitude=2.0,
            end_longitude=2.1,
            pickup_time=dt,
            travel_time=100,
            dropoff_time=dt,
            user=User.query.get(1)
        )
    try:
        # attempt to add user to db
        db.session.add(ride)
        db.session.commit()
        print "Ride created successfully"
    except exc.IntegrityError:
        print "Ride already exists"

if __name__ == '__main__':
    create_user()