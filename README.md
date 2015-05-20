# Steer-Clear-Backend
Backend and web app repo for Steer Clear app

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
