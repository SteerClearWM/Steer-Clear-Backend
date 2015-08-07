from flask import url_for
from flask.ext import testing
from steerclear import app, db
from steerclear.models import User, Ride, Role

from datetime import datetime

"""
SteerClearLoginTestCase
-----------------------
TestCase for testing the login module
"""
class SteerClearBaseTestCase(testing.TestCase):

    # do not render templates in responses
    render_templates = False

    """
    create_app
    ----------
    Creates an instance of the steerclear flask app
    and sets up testing context
    """
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['TEST_SQLALCHEMY_DATABASE_URI']
        return app

    """
    setUp
    -----
    called before each test function. creates new test database
    """
    def setUp(self):
        db.create_all()
        roles = self._create_default_roles()
        self.student_role = roles[0]
        self.admin_role = roles[1]

    """
    tearDown
    --------
    called after each test function. breaks down test fixtures
    """
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    """
    _login
    ------
    Helper function that creates a user and then logins as that user
    """
    def _login(self, user):
        self.client.post(url_for('login.login'), data={
                u'email': user.email,
                u'password': user.password,
            })

    """
    _logout
    -------
    Helper function that logs the current user out
    """
    def _logout(self):
        return self.client.get(url_for('login.logout'))

    """
    _create_user
    ------------
    Helper function that creates and returns a new User object in the db
    """
    def _create_user(self, email='ryan', password='1234', phone='+17572214000', role=None):
        if role is None:
            role = Role.query.filter_by(name='student').first()

        user = User(email=email, password=password, phone=phone, roles=[role])
        db.session.add(user)
        db.session.commit()
        return user

    """
    _create_ride
    ------------
    Helper function that creates and returns a new Ride object in the db
    """
    def _create_ride(self, user, num_passengers=0, start_latitude=1.0, start_longitude=1.1, end_latitude=2.0, end_longitude=2.1, pickup_time=datetime(1,1,1), travel_time=10, dropoff_time=datetime(1,1,1)):
        ride = Ride(
            num_passengers=num_passengers,
            start_latitude=start_latitude,
            start_longitude=start_longitude,
            end_latitude=end_latitude,
            end_longitude=end_longitude,
            pickup_time=pickup_time,
            travel_time=travel_time,
            dropoff_time=dropoff_time,
            user=user
        )
        db.session.add(ride)
        db.session.commit()
        return ride

    """
    _create_role
    ------------
    Creates a new Role in the db
    """
    def _create_role(self, name, description):
        role = Role(name=name, description=description)
        db.session.add(role)
        db.session.commit()
        return role

    """
    _create_default_roles
    ---------------------
    Creates the default student and admin Roles
    """
    def _create_default_roles(self):
        student_role = Role.query.filter_by(name='student').first()
        admin_role = Role.query.filter_by(name='admin').first()

        # create student Role
        if student_role is None:
            student_role = self._create_role('student', 'Student Role')
        # create admin Role
        if admin_role is None:
            admin_role = self._create_role('admin', 'Admin Role')
        return student_role, admin_role

    def _test_url_requires_role(self, method, url, role):
        r = Role.query.filter_by(name=role).first()

        foo_role = self._create_role('foo', 'Foo Role')
        user = self._create_user(email='foo', role=foo_role)
        self._login(user)

        response = method(url)
        self.assertEquals(response.status_code, 403)

        user = self._create_user(email='correct', role=r)
        self._login(user)

        response = method(url)
        self.assertNotEquals(response.status_code, 403)

