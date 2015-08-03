# Steer-Clear-Backend
Backend and web app repo for Steer Clear app

## TODO

* Replace temp secret key with secure key

* Create custom api exceptions

* add error checking/exception handling for database operations

* add api key for google distancematrix api

##Setup and Installation
`clone` project and `cd` into directory

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

App will now be accesible through `localhost:5000`

**NOTE:** You need the default_settings.py config file for backend to work. Get from one of the repo overseers. Alternatively, you can create your own default settings file and fill in the corresponding values using the example default settings file

##Testing

To run tests use **nosetests**

`$ nosetests`

## Helpful Scripts
There a few helpful scripts for doing things such as creating a new user or ride request

### create_db.py
* Creates and sets up the database
* **NOTE: THIS WILL DELETE ALL DATA CURRENTLY IN THE DATABASE**
* **TODO:** Change to use database migration

### /scripts/hail_ride.py
* Creates a new ride request object by making http requests to the server
* **server must be running**

### /scripts/notify_user.py
* Send a notification to a Ride requests' User by making http requests to the server
* **server must be running**

### /scripts/create_user.py
* Creates a new User
* Prompts for username/password input
* Displays message if user already exists

### /scripts/create_ride.py
* Creates a new Ride request

## Login
At the Moment, login is done with a username and password. We will be switching to just using an email address and a per session random cookie for login later.

### GET /login
* Returns the login page

### POST /login
* Route to actually log a user in
* Takes a form with a **email** and **password** field. 
* On success, redirects to **index** page.
* On failure, returns login page again

### GET /logout
* **requires user to be logged in**
* Logs the current user out of the system

## Registering Users
You can register a new user (assuming the user does not already exist) by making a simple POST request with a username and password field

### GET /register
* Returns the register page

### POST /register
* Creates a new user. 
* Takes a form with a **email** and **password** and a **phone** field.
* **phone** field must be a valid phone number string (i.e. +1xxxyyyzzzz) 
* If the user already exists return the register page again and a 409 status code
* **TODO** add error message

## Driver Portal
Desktop app that allows steerclear drivers to log in and manage the queue of ride requests

### GET /index
* **requires driver be logged in**
* Returns the ride request queue management page (not really implemented yet)

## API
* All API routes require that the user be logged in
* All API routes are prefixed by **/api/**

## Ride Request Objects
Ride request objects have several fields:

* **id**: id number of the ride object in the queue

* **num_passengers**: number of passengers in the ride request

* **start_latitude**: latitude coordinate for the pickup location

* **start_longitude**: longitude coordinate for the pickup location

* **end_latitude**: latitude coordinate for the dropoff location

* **end_longitude**: longitude coordinate for the dropoff location

* **pickup_time**: estimated pickup time as a datetime object

* **travel_time**: estimated time it will take in seconds to go from pickup location to dropoff location

* **dropoff_time**: estimated time for arriving at the dropoff location as a datetime object

## Rides
API endpoint for getting, updating, and deleting ride requests

### GET /api/rides/<int:ride_id>
Sample request **GET /api/rides/2**:

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

* Returns the ride request object with the corresponding **ride_id**
* **ride_id** is an integer
* returns 404 if the ride request does not exist

### DELETE /api/rides/<int:ride_id>
* Deletes the ride request with id **ride_id**
* Returns status code 204 on success
* If there is no ride request object with the  **ride_id**, return 404

## RideList
API endpoint for getting the lists of all ride requests or creating a new ride request.

### GET /api/rides
Sample Response:

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

* Returns the queue of ride requests as a json object

### POST /api/rides
* Creates a new ride request
* Returns the created ride object on success (this will most likely change to just returning the created ride id).
* returns error code 400 on failure
* Expects a form with the following fields
  * **id**: id number of the ride object in the queue

  * **num_passengers**: number of passengers in the ride request

  * **start_latitude**: latitude coordinate for the pickup location

  * **start_longitude**: longitude coordinate for the pickup location

  * **end_latitude**: latitude coordinate for the dropoff location

  * **end_longitude**: longitude coordinate for the dropoff location

  * **pickup_time**: estimated pickup time. See note below for string format

  * **travel_time**: estimated time it will take in seconds to go from pickup location to dropoff location

  * **dropoff_time**: estimated time for arriving at the dropoff location. see note below for string format

  * **NOTE**: the **pickup_time** and **dropoff_time** fields are datetime objects representing UTC times that are formatted as strings using the following format string **"%a, %d %b %Y %H:%M:%S GMT"**. Where **%a** is the weekday's abreviated name (i.e. Mon), **%d** is the day of the month as a zero-padded decimal number (i.e. 09 and 22), **%b** is the month's abreviated name (i.e. Sep), **%Y** is the four digit year value (i.e. 2015), **%H** is the hour zero-padded hour value (i.e. 02 or 20), **%M** is the zero-padded minute value (i.e. 05 or 52), and **%S** is the zero-padded seconds value (i.e. 06 or 33).


## Notifications
API endpoint for sending sms notifications to Users. At the moment, sms messages will only be sent successfully to Users who have verified their phone number with the SteerClear Twilio account

### POST /api/notifications
* Sends an sms message to a User
* takes a **ride_id** field which is the integer of the Ride object you wish to notify. (The User who made the Ride object is stored in the Ride object so we get which User to notify from the Ride object)
* On success, returns 201 status code
* On Failure, returns 400 or 500

