from flask import Blueprint, request
from flask_restful import Resource, Api, fields, marshal, abort
from flask.ext.login import login_required, current_user
from datetime import datetime, timedelta
from sqlalchemy import exc

from steerclear.utils.eta import time_between_locations
from steerclear import sms_client

from steerclear.utils.permissions import (
    student_permission, 
    admin_permission, 
    student_or_admin_permission,
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
    """
    @admin_permission.require(http_exception=403)
    def get(self):
        rides = Ride.query.all()                            # query db for Rides
        rides = map(Ride.as_dict, rides)                    # convert all Rides to dictionaries
        return {'rides': marshal(rides, ride_fields)}, 200  # return response

    """
    Create a new Ride object and place it in the queue
    """
    @student_or_admin_permission.require(http_exception=403)
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

    # Require that user must be logged in and
    # that the user is a student or admin
    method_decorators = [
        login_required
    ]

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
    # that the user is a student or admin
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