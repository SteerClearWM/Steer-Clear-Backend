from flask import Blueprint, request
from flask_restful import Resource, Api, fields, marshal, abort
from flask.ext.login import login_required, current_user
from datetime import datetime, timedelta
from sqlalchemy import exc

from steerclear.utils.eta import time_between_locations
from steerclear import sms_client, dm_client

from steerclear.utils.permissions import (
    student_permission, 
    admin_permission, 
    AccessRidePermission
)

from models import *
from forms import *

# set up api blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp)

# response format for Ride objects
ride_fields = {
    'id': fields.Integer(),
    'num_passengers': fields.Integer(),
    'start_latitude': fields.Float(),
    'start_longitude': fields.Float(),
    'end_latitude': fields.Float(),
    'end_longitude': fields.Float(),
    'pickup_time': fields.DateTime(dt_format='rfc822'),
    'travel_time': fields.Integer(),
    'dropoff_time': fields.DateTime(dt_format='rfc822'), 
}

"""
RideListAPI
-----------
HTTP commands for interfacing with a list of
ride objects. uri: /rides
"""
class RideListAPI(Resource):

    # Require that users be logged in in order to access the RideListAPI
    method_decorators = [login_required]

    """
    Return the list of Ride objects in the queue

    User must be an admin to access route
    """
    @admin_permission.require(http_exception=403)
    def get(self):
        rides = Ride.query.all()                            # query db for Rides
        rides = map(Ride.as_dict, rides)                    # convert all Rides to dictionaries
        return {'rides': marshal(rides, ride_fields)}, 200  # return response

    """
    Create a new Ride object and place it in the queue
    """
    def post(self):
        form = RideForm()                       # validate RideForm or 404
        if not form.validate_on_submit():
            abort(400)
        
        # get pickup and dropoff locations of Ride request
        pickup_loc = (form.start_latitude.data, form.start_longitude.data)
        dropoff_loc = (form.end_latitude.data, form.end_longitude.data)

        # query distance matrix api and get eta time data and addresses
        result = query_distance_matrix_api(pickup_loc, dropoff_loc)
        if result is None:
            abort(400)

        # get pickup, travel, and dropoff times
        pickup_time, travel_time, dropoff_time = result[0]

        # get pickup and dropoff addresses
        pickup_address, dropoff_address = result[1]
        
        # create new Ride object
        new_ride = Ride(
            num_passengers=form.num_passengers.data,
            start_latitude=form.start_latitude.data,
            start_longitude=form.start_longitude.data,
            end_latitude=form.end_latitude.data,
            end_longitude=form.end_longitude.data,
            pickup_time=pickup_time,
            travel_time=travel_time,
            dropoff_time=dropoff_time,
            user=current_user
        )
        
        try:
            db.session.add(new_ride)    # add new Ride object to db
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            abort(400)
        return {'ride': marshal(new_ride.as_dict(), ride_fields)}, 201

"""
RideAPI
-------
HTTP commands for interfacing with a single Ride object
uri: /rides/<ride_id>
"""
class RideAPI(Resource):

    # Require that user must be logged in
    method_decorators = [login_required]

    """
    Return the Ride object with the corresponding id as
    object or 404
    """
    def get(self, ride_id):
        # Check if current user is an admin or has
        # permission to access the specified Ride resource
        permission = AccessRidePermission(ride_id)
        if not permission.can() and not admin_permission.can():
            # If user doesn't have permission to access ride resource, abort 403
            abort(403)
        
        ride = Ride.query.get(ride_id)                  # query db for Ride
        if ride is None:                                # 404 if Ride does not exist
            abort(404)
        
        return {'ride': marshal(ride.as_dict(), ride_fields)}, 200

    """
    Delete a specific Ride object
    """
    def delete(self, ride_id):
        # Check if current user is an admin or has
        # permission to access the specified Ride resource
        permission = AccessRidePermission(ride_id)
        if not permission.can() and not admin_permission.can():
            # If user doesn't have permission to access ride resource, abort 403
            abort(403)
        
        ride = Ride.query.get(ride_id)  # query db for Ride object
        if ride is None:                # 404 if not found
            abort(404)
        
        try:
            db.session.delete(ride)     # attempt to delete Ride object from db
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            abort(404)
        
        return "", 204

"""
NotificationAPI
---------------
HTTP commands for sending sms messages to users
uri: /notifications
"""
class NotificationAPI(Resource):
    
    # Require that user must be logged in and
    # that the user is an admin
    method_decorators = [
        admin_permission.require(http_exception=403),
        login_required
    ]

    """
    Send an sms message to notify the user
    """
    def post(self):
        # validate that required form fields were submitted
        form = NotificationForm()
        if not form.validate_on_submit():
            abort(400)
        
        # get user who made Ride request
        ride = Ride.query.get(form.ride_id.data)
        if ride is None:
            abort(400)
        if ride.user is None or ride.user.phone is None:
            abort(500)

        # send sms message to user
        message = sms_client.notify_user(ride.user.phone.e164, message="Your Ride is Here!") 
        if message is None:
            abort(400)
        return '', 201

# route urls to resources
api.add_resource(RideListAPI, '/rides', endpoint='rides')
api.add_resource(RideAPI, '/rides/<int:ride_id>', endpoint='ride')
api.add_resource(NotificationAPI, '/notifications', endpoint='notifications')

"""
query_distance_matrix_api
-------------------
Takes a pickup and dropoff location for a Ride request
and returns the pickup, travel, and dropoff times
"""
def query_distance_matrix_api(pickup_loc, dropoff_loc):
    # check to see if there are any rides in the queue
    last_ride = db.session.query(Ride).order_by(Ride.id.desc()).first()

    # if there are no rides in the queue, pickup_loc and
    # dropoff_loc are our only destinations
    if last_ride is None:
        # eta = time_between_locations([pickup_loc], [dropoff_loc])

        # query google distance matrix api and get response
        response = dm_client.query_api([pickup_loc], [dropoff_loc])
        
        # get eta or return None
        eta = response.get_eta()
        if eta is None:
            return None
       
        # calculate pickup, travel, and dropoff times based off eta response
        # assumes that van will arive at pickup_loc within 5 minutes
        pickup_time = datetime.utcnow() + timedelta(0, 10 * 60)
        travel_time = eta[0][0]
        dropoff_time = pickup_time + timedelta(0, travel_time)

        # get addresses or return None
        addresses = response.get_addresses()
        if addresses is None:
            return None

        # get pickup and dropoff addresses.
        # pickup address is the first address in origin_addresses (index 0)
        # dropoff address is the first address in destination_addresses (index 1)
        pickup_address = addresses[0][0]
        dropoff_address = addresses[1][0]
    
    # else there are other rides in the queue, so we must factor
    # in the dropoff time and location from the last ride in the queue
    else:
        # get last ride dropoff location. this is our starting location
        start_loc = (last_ride.end_latitude, last_ride.end_longitude)

        # query google distance matrix api and get response
        response = dm_client.query_api([start_loc, pickup_loc], [pickup_loc, dropoff_loc])
        
        # get eta or return None
        eta = response.get_eta()
        if eta is None:
            return None

        # get addresses or return None
        addresses = response.get_addresses()
        if addresses is None:
            return None
        
        # calculate pickup, travel, and dropoff times based off eta response
        pickup_time = last_ride.dropoff_time + timedelta(0, eta[0][0])
        travel_time = eta[1][1]
        dropoff_time = pickup_time + timedelta(0, travel_time)

        # get pickup and dropoff addresses.
        # pickup address is the second address in origin_addresses (index 0)
        # dropoff address is the second address in destination_addresses (index 1)
        pickup_address = addresses[0][1]
        dropoff_address = addresses[1][1]
    
    return (pickup_time, travel_time, dropoff_time), (pickup_address, dropoff_address)

@api_bp.route('/clear')
def clear():
    db.session.query(Ride).delete()
    db.session.commit()
    return "OK"