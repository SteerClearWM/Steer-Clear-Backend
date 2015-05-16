#Routes

routing parameters for steerclear backend api

## /

Simple check to see if server is running. Should return the string "pulse" and status code 200

## /rides

URL for interacting with the ride queue. can list all rides or add a ride

### GET /rides

returns a json object of the list of all rides. Sample:
{
  "rides": [
    {
      "end_latitude": 1.01, 
      "end_longitude": 5.07, 
      "id": 1, 
      "num_passengers": 4, 
      "phone_number": "aaa-aaa-aaaa", 
      "start_latitude": 10.0, 
      "start_longitude": 50.1
    }, 
    {
      "end_latitude": 1.01, 
      "end_longitude": 5.07, 
      "id": 2, 
      "num_passengers": 4, 
      "phone_number": "aaa-aaa-aaaa", 
      "start_latitude": 10.0, 
      "start_longitude": 50.1
    }
  ]
}

### POST rides

Add a ride to the queue. Payload must have the following data fields:

**phone_number**: phone number in string format
**num_passengers**: integer value of the number of passengers in ride
**start_latitude**: floating point latitude value of start location
**start_longitude**: floating point longitude value of start location
**end_latitude**: floating point latitude value of end location
**end_longitude**: floating point longitude value of end location

## /clear

Clears and empties the ride queue