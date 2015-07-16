from flask import Blueprint, request, json
from flask_restful import Resource, Api, abort
from models import *
from forms import *
from eta import time_between_locations
from datetime import datetime, timedelta
from sqlalchemy import exc

# set up api blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp)

"""
RideListAPI
-----------
HTTP commands for interfacing with a list of
ride objects. uri: /rides
"""
class RideListAPI(Resource):
    """
    Return the list of Ride objects in the queue
    """
    def get(self):
        rides = Ride.query.all()                # query db for Rides
        rides = map(Ride.as_dict, rides)        # convert all Rides to dictionaries
        return json.jsonify({'rides': rides})   # return response

    """
    Create a new Ride object and place it in the queue
    """
    def post(self):
        form = RideForm()                       # validate RideForm or 404
        if not form.validate_on_submit():
            abort(400)
        
        # calculate pickup and dropoff time
        pickup_loc = (form.start_latitude.data, form.start_longitude.data)
        dropoff_loc = (form.end_latitude.data, form.end_longitude.data)
        time_data = calculate_time_data(pickup_loc, dropoff_loc)
        if time_data is None:
            abort(400)
        
        # create new Ride object
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
            db.session.add(new_ride)    # add new Ride object to db
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            abort(400)
        return json.jsonify({'ride': new_ride.as_dict()})

"""
RideAPI
-------
HTTP commands for interfacing with a single Ride object
uri: /rides/<ride_id>
"""
class RideAPI(Resource):
    """
    Return the Ride object with the corresponding id as
    a json object or 404
    """
    def get(self, ride_id):
        ride = Ride.query.get(ride_id)                  # query db for Ride
        if ride is None:                                # 404 if Ride does not exist
            abort(404)
        return json.jsonify({'ride': ride.as_dict()})

    """
    Delete a specific Ride object
    """
    def delete(self, ride_id):
        ride = Ride.query.get(ride_id)  # query db for Ride object
        if ride is None:                # 404 if not found
            abort(404)
        try:
            db.session.delete(ride)     # attempt to delete Ride object from db
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            abort(404)
        return "OK"

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

@api_bp.route('/clear')
def clear():
    db.session.query(Ride).delete()
    db.session.commit()
    return "OK"