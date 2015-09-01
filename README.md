# Steer-Clear-Backend
Backend and web app for Steer Clear student ride request service

## TODO

* Add ride queue filtering by on/off campus

* Change using Floats to store lat/long to using Decimals

* Write tests for cookie remember duration

* Make sure student users can't access ride queue page

* Replace temp secret key with secure key

* Create custom api exceptions

* add api key for google distancematrix api

##Database Setup and Configuration

You need to install the mysql-server and mysql-client

Start the mysql server

    # On Linux
    $ sudo service mysql start

    # On Mac
    $ sudo mysql.server start

    # Another way on Mac
    $ sudo /usr/local/mysql/bin/mysqld_safe

    # On Windows
    $ "C:\Program Files\MySQL\MySQL Server 5.0\bin\mysqld"

Use the mysql client to login as the root user of the mysql server and create 2 databases. 1 for production and 1 for testing

**Optional:** Create a new user who has privileges over the 2 databases

The script **/scripts/setup_db.sql** will create 2 databases (**db** and **test**) and a new user (**steerclear** with password **St33rCl3@r**) automatically. To run it, use the mysql client as the root user
    
    # On both Windows and Mac/Linux
    $ mysql -u root -p < scripts/setup_db.sql
    Enter Password: root_user_password_here

In *steerclear/settings/default_settings.py replace the following with your mysql user username, password, and database names

    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://username:password@localhost/db_name'
    TEST_SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://username:password@localhost/test_db_name'

If you ran the setup_db.sql script it should look like the first 2 lines in **/steerclear/settings/default_settings_example.py:**
    
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://steerclear:St33rCl3@r@localhost/db'
    TEST_SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://steerclear:St33rCl3@r@localhost/test'

Since we are using mysql, you might need to specify the amount of time database connections are allowed to be idle before being refreshed (http://docs.sqlalchemy.org/en/rel_1_0/core/pooling.html#setting-pool-recycle). There is a flag in steerclear/settings/default_settings.py that you can modify

##Setup and Installation
`clone` project and `cd` into directory

Create virtualenv

`$ virtualenv --no-site-packages env`

Activate virtualenv

`$ source env/bin/activate`

Install requirements

`$ pip install -r requirements.txt`

Create/Sync Database

    $ python migrate.py db migrate
    $ python migrate.py db upgrade

Check that all tests pass

`$ nosetests`

Run app

    # will run server on port 5000 by default
    $ python runserver.py
    
    # will run server on specified port number and in debug mode
    $ python runserver.py --port port_number --debug

***NOTE:** You need the default_settings.py config file for backend to work. Get from one of the repo overseers. Alternatively, you can create your own default settings file and fill in the corresponding values using **steerclear/settings/default_settings_example.py** file as a template

##Testing

To run tests use **nosetests**

`$ nosetests`

## Helpful Scripts
There a few helpful scripts for doing things such as creating a new user or ride request

### /scripts/setup_db.sql
* Creates the production and test databases

* creates a new user, **steerclear**, that has privileges over both databases
* **mysql server must be running**

### /scripts/create_db.py
* Creates and sets up the data model tables in the database
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
* Prompts for username/phone/role input
* Displays message if user already exists

### /scripts/create_ride.py
* Creates a new Ride request

## Login
Login is done with a valid w&m account username and password. 

### GET /login
* Returns the login page

### POST /login
* Route to actually log a user in
* Takes a form with a **username** and **password** field. 
* On success, redirects to **index** page.
* On failure, returns login page again and 400 status code

### GET /logout
* **requires user to be logged in**
* Logs the current user out of the system

## Registering Users
You can register a new user (assuming the user does not already exist) by making a simple POST request with a username, password, and phone field. The new user will have all api permissions that a student has

### POST /register
* Creates a new user. 
* Takes a form with a **username** and **password** and a **phone** field.
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
* Some API routes require the user to have certain permissions (e.x. be a student, be an admin, etc...)

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

* **pickup_address**: the string address of the pickup location for the request

* **dropoff_address**: the string address of the dropoff location for the request

* **on_campus**: boolean flag indicating if a ride request is on campus or off campus. On campus rides are classified as rides whose **pickup_loc** is on the main wm campus

## Rides
API endpoint for getting, updating, and deleting ride requests. student users are only allowed to access ride requests they have requested. If a student attempts to access a ride request they have not placed, a 403 is returned

### GET /api/rides/<int:ride_id>
Sample request **GET /api/rides/2**:

    "ride": {
        "dropoff_address": "1234 Richmond Road, Williamsburg, VA 23185, USA", 
        "dropoff_time": "Wed, 12 Aug 2015 05:33:08 -0000", 
        "end_latitude": 37.2809, 
        "end_longitude": -76.7197, 
        "id": 1, 
        "num_passengers": 3, 
        "pickup_address": "2006 Brooks Street, Williamsburg, VA 23185, USA", 
        "pickup_time": "Wed, 12 Aug 2015 05:29:09 -0000", 
        "start_latitude": 37.2735, 
        "start_longitude": -76.7196, 
        "travel_time": 239,
        "on_campus": true
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
                "dropoff_address": "1234 Richmond Road, Williamsburg, VA 23185, USA", 
                "dropoff_time": "Wed, 12 Aug 2015 05:33:08 -0000", 
                "end_latitude": 37.2809, 
                "end_longitude": -76.7197, 
                "id": 1, 
                "num_passengers": 3, 
                "pickup_address": "2006 Brooks Street, Williamsburg, VA 23185, USA", 
                "pickup_time": "Wed, 12 Aug 2015 05:29:09 -0000", 
                "start_latitude": 37.2735, 
                "start_longitude": -76.7196, 
                "travel_time": 239,
                "on_campus": true
            }, 
            {
                "dropoff_address": "1234 Richmond Road, Williamsburg, VA 23185, USA", 
                "dropoff_time": "Wed, 12 Aug 2015 05:40:34 -0000", 
                "end_latitude": 37.2809, 
                "end_longitude": -76.7197, 
                "id": 2, 
                "num_passengers": 3, 
                "pickup_address": "2006 Brooks Street, Williamsburg, VA 23185, USA", 
                "pickup_time": "Wed, 12 Aug 2015 05:36:35 -0000", 
                "start_latitude": 37.2735, 
                "start_longitude": -76.7196, 
                "travel_time": 239,
                "on_campus": true
            }
        ]
    }

* Returns the queue of ride requests as a json object

### GET /api/rides?location=[on_campus | off_campus]
* If you add the **location** query string parameter, you can filter the ride requests that are returned to you

* setting **location=on_campus** returns the list of ride requests that are on campus

* setting **location=off_campus** returns the list of ride requests that are off campus

### POST /api/rides
* **only admin users can access this route**
* Creates a new ride request
* Returns the created ride object on success (this will most likely change to just returning the created ride id).
* returns error code 400 on failure
* Expects a form with the following fields


  * **num_passengers**: number of passengers in the ride request

  * **start_latitude**: latitude coordinate for the pickup location

  * **start_longitude**: longitude coordinate for the pickup location

  * **end_latitude**: latitude coordinate for the dropoff location

  * **end_longitude**: longitude coordinate for the dropoff location

## Notifications
API endpoint for sending sms notifications to Users. At the moment, sms messages will only be sent successfully to Users who have verified their phone number with the SteerClear Twilio account

### POST /api/notifications
* **only admin users can access this route**
* Sends an sms message to a User
* takes a **ride_id** field which is the integer of the Ride object you wish to notify. (The User who made the Ride object is stored in the Ride object so we get which User to notify from the Ride object)
* On success, returns 201 status code
* On Failure, returns 400 or 500

