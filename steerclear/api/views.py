from flask import Blueprint, request, json
from flask_restful import Resource, Api, abort
from models import *
from forms import *
from eta import time_between_locations
from datetime import datetime, timedelta
from sqlalchemy import exc

api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp)

class RideListAPI(Resource):
    def get(self):
        rides = Ride.query.all()
        rides = map(Ride.as_dict, rides)
        return json.jsonify({'rides': rides})

    def post(self):
        form = RideForm()
        if not form.validate_on_submit():
            abort(404)
        
        pickup_loc = (form.start_latitude.data, form.start_longitude.data)
        dropoff_loc = (form.end_latitude.data, form.end_longitude.data)
        time_data = calculate_time_data(pickup_loc, dropoff_loc)
        if time_data is None:
            abort(404)
        
        pickup_time, travel_time, dropoff_time = time_data
        new_ride = Ride(
            form.num_passengers.data,
            pickup_loc,
            dropoff_loc,
            pickup_time,
            travel_time,
            dropoff_time
        )
        
        try:
            db.session.add(new_ride)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            abort(404)
        return json.jsonify({'ride': new_ride.as_dict()})

class RideAPI(Resource):
    def get(self, ride_id):
        ride = Ride.query.get(ride_id)
        if ride is None:
            abort(404)
        return json.jsonify({'ride': ride.as_dict()})

api.add_resource(RideListAPI, '/rides')
api.add_resource(RideAPI, '/rides/<int:ride_id>')

def calculate_time_data(pickup_loc, dropoff_loc):
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
rides
-----
View for handling all ride functionality.
If it is a GET request, return the queue of rides
as a json object. If the method is POST, add a new ride
to the queue and return the ride json object in the response
"""
@api_bp.route('/rides/<int:ride_id>', methods=['PUT', 'DELETE'])
def rides(ride_id=None):
    if request.method == 'DELETE':
        return make_delete_ride(ride_id)
    if request.method == 'PUT':
        return "asd;lfkjasd"

@api_bp.route('/clear')
def clear():
    db.session.query(Ride).delete()
    db.session.commit()
    return "OK"