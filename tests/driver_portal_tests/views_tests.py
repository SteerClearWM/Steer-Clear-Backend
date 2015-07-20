from steerclear import app, db
from steerclear.models import User
from flask.ext import testing
from flask import url_for

"""
SteerClearTestCase
------------------
TestCase for driver side management
"""
class SteerClearTestCase(testing.TestCase):

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
    called before each test function. Sets up flask app test
    instance and creates new test database
    """
    def setUp(self):
        db.create_all()

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
    def _login(self):
        user = User(username='ryan', password='1234')
        db.session.add(user)
        db.session.commit()
        self.client.post(url_for('login.login'), data={
                u'username': u'ryan',
                u'password': u'1234'
            })

    """
    test_heartbeat
    --------------
    tests that server is up and running and that the
    '/' route returns a 200 status code and "pulse"
    """
    def test_heartbeat(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.get_data(), "pulse")

    """
    test_get_index_requires_login
    -----------------------------
    Tests that index page requires login
    """
    def test_get_index_requires_login(self):
        response = self.client.get(url_for('driver_portal.index'))
        self.assertEquals(response.status_code, 401)

    """
    test_get_index
    --------------
    Tests that only logged in users can access the index page
    """
    def test_get_index(self):
        self._login()
        response = self.client.get(url_for('driver_portal.index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('index.html')

