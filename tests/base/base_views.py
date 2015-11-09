from flask import url_for
from flask.ext import testing
from steerclear import app, db
from steerclear.models import User, Ride, Role, TimeLock
from testfixtures import Replacer

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
        timelock = TimeLock(state=True)
        db.session.add(timelock)
        db.session.commit()

        self.roles = self._create_default_roles()
        self.student_role = self.roles[0]
        self.admin_role = self.roles[1]
        self.foo_role = self.roles[2]

        self.student_user = self._create_user(username='student', phone='+12223334444', role=self.student_role)
        self.admin_user = self._create_user(username='admin', phone='+13334445555', role=self.admin_role)
        self.foo_user = self._create_user(username='foo', phone='+14445556666', role=self.foo_role)
        self.student_user2 = self._create_user(username='student2', phone='+15556667777', role=self.student_role)

        self.users = [self.student_user, self.admin_user, self.foo_user]

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
        with Replacer() as r:
            r.replace('steerclear.utils.cas.validate_user', self.mock_validate_user)
            self.client.post(url_for('login.login'), data={
                    u'username': user.username,
                    u'password': '1234',
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
    def _create_user(self, username='ryan', phone='+17572214000', role=None):
        if role is None:
            role = Role.query.filter_by(name='student').first()

        user = User(username=username, phone=phone, roles=[role])
        db.session.add(user)
        db.session.commit()
        return user

    """
    _create_ride
    ------------
    Helper function that creates and returns a new Ride object in the db
    """
    def _create_ride(self, user, num_passengers=0, start_latitude=1.0, start_longitude=1.1, end_latitude=2.0, end_longitude=2.1, pickup_time=datetime(1,1,1), travel_time=10, dropoff_time=datetime(1,1,1), pickup_address='Foo', dropoff_address='Bar', on_campus=True):
        ride = Ride(
            num_passengers=num_passengers,
            start_latitude=start_latitude,
            start_longitude=start_longitude,
            end_latitude=end_latitude,
            end_longitude=end_longitude,
            pickup_time=pickup_time,
            travel_time=travel_time,
            dropoff_time=dropoff_time,
            pickup_address=pickup_address,
            dropoff_address=dropoff_address,
            on_campus=on_campus,
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
        foo_role = Role.query.filter_by(name='foo').first()

        # create student Role
        if student_role is None:
            student_role = self._create_role('student', 'Student Role')
        # create admin Role
        if admin_role is None:
            admin_role = self._create_role('admin', 'Admin Role')
        # create foo Role
        if foo_role is None:
            foo_role = self._create_role('foo', 'Foo Role')
        return student_role, admin_role, foo_role

    """
    _test_url_requires_roles
    ------------------------
    Tests that the :url: accessed via the http :method:
    is available to all users with any role in :roles:
    and unavailable to all other users
    """
    def _test_url_requires_roles(self, method, url, roles):
        # for every user
        for user in self.users:
            # login the user and make request to url
            self._login(user)
            response = method(url)

            # check to see if user has any role that should have permission for url
            for role in user.roles:
                if role in roles:
                    # if the user should have permission, make sure response code is not 403
                    self.assertNotEquals(response.status_code, 403)
                    break
                else:
                    # if the user shouldn't have permission, make sure status code is 403
                    self.assertEquals(response.status_code, 403)
                    break

    def _change_timelock(self, new_state):
        timelock = TimeLock.query.first()
        timelock.state = new_state
        db.session.commit()

    """
    mock_validate_user
    ------------------
    Mock method for replacing validate_user() so that it always returns true
    """
    def mock_validate_user(self, username, password):
        return True
