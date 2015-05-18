from steerclear import app
from flask import request, json, abort
from models import *
from forms import *

def list_rides():
    result = Ride.query.all()
    return map(Ride.as_dict, result)

@app.errorhandler(404)
def resource_not_found(error):
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
def rides():
    if request.method == 'GET':
        ride_list = list_rides()
        return json.jsonify({'rides': ride_list})

    form = RideForm()
    new_ride = form.as_ride()                               # convert form to Ride object
    if request.method == 'POST' and form.validate_on_submit():  # validate form data
        db.session.add(new_ride)                                # and and commit new ride object to database
        db.session.commit()
        return json.jsonify({'ride': new_ride.as_dict()})
    
    return json.jsonify({'ride': new_ride.as_dict()}), 404

@app.route('/clear')
def clear():
    db.session.query(Ride).delete()
    db.session.commit()
    return "OK"
