from steerclear import app
from flask import request, json, abort
from models import *

def list_rides():
	result = Ride.query.all()
	return map(Ride.as_dict, result)

def add_ride(phone_number, num_passengers, pickup, dropoff):
	new_ride = Ride(phone_number, num_passengers, pickup, dropoff)
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


	data = request.form

	# for k, v in data:
	# 	if not v:
	# 		abort(404)

	phone_number = data.get('phone_number', '')
	if not phone_number:
		abort(404)

	num_passengers = data.get('num_passengers', '')
	if not num_passengers:
		abort(404)

	start_latitude = data.get('start_latitude', '')
	if not start_latitude:
		abort(404)

	start_longitude = data.get('start_longitude', '')
	if not start_longitude:
		abort(404)

	end_latitude = data.get('end_latitude', '')
	if not end_latitude:
		abort(404)

	end_longitude = data.get('end_longitude', '')
	if not end_longitude:
		abort(404)

	pickup = (start_latitude, start_longitude)
	dropoff = (end_latitude, end_longitude)
	new_ride = add_ride(phone_number, num_passengers, pickup, dropoff)
	return json.jsonify({'ride': new_ride})

