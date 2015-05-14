from steerclear import app
from flask import request, json, abort
from models import *

def list_rides():
	result = Ride.query.all()
	return map(Ride.as_dict, result)

def add_ride(name, phone_number):
	new_ride = Ride(name, phone_number)
	db.session.add(new_ride)
	db.session.commit()
	return new_ride.as_dict()


@app.route('/')
def heartbeat():
        return "pulse"

@app.route('/rides', methods=['GET', 'POST'])
def rides():
	if request.method == 'GET':
		return json.jsonify({'rides': list_rides()})
	
	print request.form
	name = request.form.get('name', '')
	print "name: " + name
	phone_number = request.form.get('phone_number', '')
	if not name or not phone_number:
		abort(404)

	new_ride = add_ride(name, phone_number)
	return json.jsonify({'ride': new_ride})

