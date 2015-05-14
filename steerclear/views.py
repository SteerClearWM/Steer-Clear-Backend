from steerclear import app
from flask import request, json
from models import *

def list_rides():
	result = Ride.query.all()
	return map(Ride.as_dict, result)




@app.route('/')
def heartbeat():
        return "pulse"

@app.route('/rides', methods=['GET', 'POST'])
def rides():
	if request.method == 'GET':
		return json.jsonify({'rides': list_rides()})
	else:
		return "new ride"

