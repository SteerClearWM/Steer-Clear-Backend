from steerclear import app
from flask import request, json, abort
from models import *
from forms import *

def list_rides():
    result = Ride.query.all()
    return map(Ride.as_dict, result)

def add_ride(ride):
    db.session.add(ride)
    db.session.commit()

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
        return json.jsonify({'rides': list_rides()})

    form = RideForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_ride = form.as_ride()
        add_ride(new_ride)
        return json.jsonify({'ride': new_ride.as_dict()})
    
    abort(404)

@app.route('/clear')
def clear():
    db.session.query(Ride).delete()
    db.session.commit()
    return "OK"
