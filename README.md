# Steer-Clear-Backend
Backend and web app repo for Steer Clear app

## TODO

* Create custom api exceptions

* add error checking/exception handling for database operations

* add api key for google distancematrix api

##Setup and Installation
Create virtualenv

`$ virtualenv --no-site-packages env`

Activate virtualenv

`$ source env/bin/activate`

Install requirements

`$ pip install -r requirements.txt`

Activate OS specific environment variables settings

    #Linux/Mac
    $ source ./scripts/setup.sh
   
    #Windows - do this is cmd not powershell. you might need to use setx instead
    > set STEERCLEAR_SETTINGS=settings\windows_settings.py

Create Database (NOTE: this will delete old database at the moment)

`$ python create_db.py`

Check that all tests pass

`$ nosetests`

Run app

`$ python runserver.py`

##Testing

To run tests use **nosetests**

`$ nosetests`

##Routes

routing parameters for steerclear backend api

### /

Simple check to see if server is running. Should return the string "pulse" and status code 200

### /rides

URL for interacting with the ride queue. can list all rides, list a single ride, add a ride, or delete a ride

#### GET /rides

returns a json object of the list of all rides. Sample:

    {
      "rides": [
        {
          "dropoff_time": "Sun, 07 Jun 2015 02:18:50 GMT", 
          "end_latitude": 37.280893, 
          "end_longitude": -76.719691, 
          "id": 1, 
          "num_passengers": 4, 
          "pickup_time": "Sun, 07 Jun 2015 02:15:59 GMT", 
          "start_latitude": 37.273485, 
          "start_longitude": -76.719628, 
          "travel_time": 171
        }, 
        {
          "dropoff_time": "Sun, 07 Jun 2015 02:24:49 GMT", 
          "end_latitude": 37.280893, 
          "end_longitude": -76.719691, 
          "id": 2, 
          "num_passengers": 4, 
          "pickup_time": "Sun, 07 Jun 2015 02:21:58 GMT", 
          "start_latitude": 37.273485, 
          "start_longitude": -76.719628, 
          "travel_time": 171
        }
      ]
    }

**id**: id number of the ride object in the queue

**num_passengers**: number of passengers in the ride request

**start_latitude**: latitude coordinate for the pickup location

**start_longitude**: longitude coordinate for the pickup location

**end_latitude**: latitude coordinate for the dropoff location

**end_longitude**: longitude coordinate for the dropoff location

**pickup_time**: estimated pickup time. See note below for string format

**travel_time**: estimated time it will take in seconds to go from pickup location to dropoff location

**dropoff_time**: estimated time for arriving at the dropoff location. see note below for string format

**NOTE**: the **pickup_time** and **dropoff_time** fields are datetime objects representing UTC times that are formatted as strings using the following format string **"%a, %d %b %Y %H:%M:%S GMT"**. Where **%a** is the weekday's abreviated name (i.e. Mon), **%d** is the day of the month as a zero-padded decimal number (i.e. 09 and 22), **%b** is the month's abreviated name (i.e. Sep), **%Y** is the four digit year value (i.e. 2015), **%H** is the hour zero-padded hour value (i.e. 02 or 20), **%M** is the zero-padded minute value (i.e. 05 or 52), and **%S** is the zero-padded seconds value (i.e. 06 or 33).

#### GET rides/<ride_id>

returns a json object for the ride object with the corresponding **<ride_id>** value or 404s if no object has the right id. Sample using request  **GET rides/2**:

    {
      "ride": {
        "dropoff_time": "Sun, 07 Jun 2015 02:24:49 GMT", 
        "end_latitude": 37.280893, 
        "end_longitude": -76.719691, 
        "id": 2, 
        "num_passengers": 4, 
        "pickup_time": "Sun, 07 Jun 2015 02:21:58 GMT", 
        "start_latitude": 37.273485, 
        "start_longitude": -76.719628, 
        "travel_time": 171
      }
    }


#### POST rides

Add a ride to the queue. On success, returns json object with created ride. On failure, returns request payload for helpful debugging. Payload must be form encoded. Payload must have the following data fields:

**num_passengers**: integer value of the number of passengers in ride

**start_latitude**: floating point latitude value of start location

**start_longitude**: floating point longitude value of start location

**end_latitude**: floating point latitude value of end location

**end_longitude**: floating point longitude value of end location

#### DELETE rides/<ride_id>

Delete a ride from the queue with cooresponding **<ride_id>**. Cancels a ride based on id. Returns "OK" 200 on success and "Sorry" 404 on failure. Example request: **DELETE /rides/4** - deletes ride object with id 4 or returns 404 if no object exists

### /clear

Clears and empties the ride queue

