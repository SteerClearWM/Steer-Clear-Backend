from steerclear import app
from flask import request, json, abort
from models import *
from forms import *

def list_rides():
    rides = Ride.query.all()
    return map(Ride.as_dict, rides)

def list_ride(ride_id):
    if ride_id is None:
        raise Exception
    ride = Ride.query.get(ride_id)
    if ride is None:
        raise Exception
    return ride.as_dict()

def hail_ride():
    form = RideForm()
    print form.data
    if not form.validate_on_submit():
        raise Exception
    new_ride = form.as_ride()
    db.session.add(new_ride)                                # and and commit new ride object to database
    db.session.commit()
    return new_ride.as_dict()

def cancel_ride(ride_id):
    if ride_id is None:
        raise Exception
    canceled_ride = Ride.query.get(ride_id)
    if canceled_ride is None:
        raise Exception

    db.session.delete(canceled_ride)
    db.session.commit()

def make_list_rides(ride_id):
    if ride_id is None:
        ride_list = list_rides()
        return json.jsonify({'rides': ride_list})
    else:
        try:
            ride = list_ride(ride_id)
            return json.jsonify({'ride': ride})
        except Exception:
            return "Sorry", 404

def make_hail_ride():
    try:
        new_ride = hail_ride()
        return json.jsonify({'ride': new_ride})
    except Exception:
        return "Sorry", 404

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
