# Steer-Clear-Backend
Backend and web app repo for Steer Clear app

## TODO

* Create custom api exceptions

* add error checking/exception handling for database operations

##Setup and Installation
Create virtualenv

`$ virtualenv --no-site-packages env`

Activate virtualenv

`$ source env/bin/activate`

Install requirements

`$ pip install -r requirements.txt`

Activate OS specific environment variables settings

    #Linux/Mac
    $ ./scripts/setup.sh
   
    #Windows
    > ./scripts/setup.bat

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

URL for interacting with the ride queue. can list all rides or add a ride

#### GET /rides

returns a json object of the list of all rides. Sample:

    {
      
      "rides": [
        
        {
          
          "end_latitude": 1.01, 
          
          "end_longitude": 5.07, 
          
          "id": 1, 
          
          "num_passengers": 4, 
                
          "start_latitude": 10.0, 
          
          "start_longitude": 50.1
        
        }, 
        
        {
        
          "end_latitude": 1.01, 
        
          "end_longitude": 5.07, 
        
          "id": 2, 
        
          "num_passengers": 4, 
            
          "start_latitude": 10.0, 
        
          "start_longitude": 50.1
        
        }
      
      ]

    }

#### POST rides

Add a ride to the queue. On success, returns json object with created ride. On failure, returns request payload for helpful debugging. Payload must be form encoded. Payload must have the following data fields:

**num_passengers**: integer value of the number of passengers in ride

**start_latitude**: floating point latitude value of start location

**start_longitude**: floating point longitude value of start location

**end_latitude**: floating point latitude value of end location

**end_longitude**: floating point longitude value of end location

#### DELETE rides

Delete a ride from the queue. Cancels a ride based on id. Returns "OK" 200 on success and "Sorry" 404 on failure. Example request:

**DELETE /rides/4** - deletes ride object with id 4 or returns 404 if no object exists

### /clear

Clears and empties the ride queue

