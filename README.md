# Steer-Clear-Backend
Backend and web app repo for Steer Clear app

##Setup and Installation
Create virtualenv

`$ virtualenv --no-site-packages env`

Activate virtualenv

`$ source env/bin/activate`

Install requirements

`$ pip install -r requirements.txt`

Create Database (NOTE: only works on Mac or Unix based systems right now)

`$ python create_db.py`

Check that all tests pass

`$ nosetests`

Run app

`$ python runserver.py`

##Testing

To run tests use **nosetests**

`$ nosetests`
