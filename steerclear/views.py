from steerclear import app
from flask import request, json, abort
from models import *
from forms import *
from eta import time_between_locations
from datetime import datetime, timedelta

def calculate_time_data(pickup_loc, dropoff_loc):
    # pickup_loc = (form.start_latitude.data, form.start_longitude.data)
    # dropoff_loc = (form.end_latitude.data, form.end_longitude.data)

    last_ride = db.session.query(Ride).order_by(Ride.id.desc()).first()
    if last_ride is None:
        eta = time_between_locations([pickup_loc], [dropoff_loc])
        if eta is None:
            return None
        pickup_time = datetime.utcnow() + timedelta(0, 10 * 60)
        travel_time = eta[0][0]
        dropoff_time = pickup_time + timedelta(0, travel_time)
    else:
        start_loc = (last_ride.end_latitude, last_ride.end_longitude)
        eta = time_between_locations([start_loc, pickup_loc], [pickup_loc, dropoff_loc])
        if eta is None:
            return None
        pickup_time = last_ride.dropoff_time + timedelta(0, eta[0][0])
        travel_time = eta[1][1]
        dropoff_time = pickup_time + timedelta(0, travel_time)
    return (pickup_time, travel_time, dropoff_time)

    # (pickup_time, travel_time, dropoff_time) = time_data
    # new_ride = Ride(
    #     form.num_passengers.data,
    #     pickup_loc,
    #     dropoff_loc,
    #     pickup_time,
    #     travel_time,
    #     dropoff_time
    # )

"""
list_rides
----------
Lists all of the rides in the ride queue.
Returns a list of Ride dictionaries
"""
def list_rides():
    rides = Ride.query.all()
    return map(Ride.as_dict, rides)

"""
list_ride
---------
List a specific ride base on ride_id.
Returns the Ride dictionary of the ride
with id *ride_id* or raises an exception if
the Ride doesn't exist
"""
def list_ride(ride_id):
    if ride_id is None:
        return None
    ride = Ride.query.get(ride_id)
    if ride is None:
        return None
    return ride.as_dict()

"""
hail_ride
---------
Creates a new Ride object and adds it to the ride queue.
Returns the created Ride dictionary.
Raises an exception if form data is invalid.
"""
def hail_ride():
    form = RideForm()
    if not form.validate_on_submit():
        return None
    new_ride = Ride(
        form.num_passengers.data,
        (form.start_latitude.data, form.start_longitude.data),
        (form.end_latitude.data, form.end_longitude.data),
        datetime(1,1,1),
        0,
        datetime(1,1,1)
    )
    db.session.add(new_ride)
    db.session.commit()
    return new_ride.as_dict()

"""
cancel_ride
-----------
Removes a ride with a specific *ride_id* from the ride queue.
Raises an exception if *ride_id* is None or if no Ride exists
"""
def cancel_ride(ride_id):
    if ride_id is None:
        raise Exception
    canceled_ride = Ride.query.get(ride_id)
    if canceled_ride is None:
        raise Exception

    db.session.delete(canceled_ride)
    db.session.commit()

"""
make_list_rides
---------------
Wrapper for listing the ride queue or a single ride.
"""
def make_list_rides(ride_id):
    if ride_id is None:
        ride_list = list_rides()
        return json.jsonify({'rides': ride_list})
    ride = list_ride(ride_id)
    if ride is None:
        return "Sorry", 404
    return json.jsonify({'ride': ride})

"""
make_hail_ride
--------------
Wrapper for hailing a ride
"""
def make_hail_ride():
    new_ride = hail_ride()
    if new_ride is None:
        return "Sorry", 404
    return json.jsonify({'ride': new_ride})

"""
make_delete_ride
----------------
Wrapper for canceling a ride
"""
def make_delete_ride(ride_id):
    try:
        cancel_ride(ride_id)
        return "OK"
    except Exception:
        return "Sorry", 404

"""
heartbeat
---------
Simple check to see if server is running
"""
@app.route('/')
def heartbeat():
        return "pulse"

"""
rides
-----
View for handling all ride functionality.
If it is a GET request, return the queue of rides
as a json object. If the method is POST, add a new ride
to the queue and return the ride json object in the response
"""
@app.route('/rides', methods=['GET', 'POST'])
@app.route('/rides/<int:ride_id>', methods=['GET', 'PUT', 'DELETE'])
def rides(ride_id=None):
    if request.method == 'GET':
        return make_list_rides(ride_id)
    if request.method == 'POST':
        return make_hail_ride()
    if request.method == 'DELETE':
        return make_delete_ride(ride_id)
    if request.method == 'PUT':
        return "asd;lfkjasd"

@app.route('/clear')
def clear():
    db.session.query(Ride).delete()
    db.session.commit()
    return "OK"
