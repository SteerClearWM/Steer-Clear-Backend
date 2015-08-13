"""
cas.py
By: Ryan Beatty

Enable automatic login to W&M CAS server by emulating
a browser to perform login
"""
import mechanize
from urllib2 import HTTPError

# url of the login route for the W&M CAS server
WM_CAS_SERVER_URL = 'https://cas.wm.edu/cas/login?service=http%3A//localhost%3A8080/login/'

"""
validate_user
-------------
Checks if a Users' email and password credentials are valid,
meaning that they are a valid W&M student and can use the
steerclear service
"""
def validate_user(email, password):
    # create new browser object
    browser = mechanize.Browser()

    # disable robots.txt and automatic redirects
    # disabling redirects means that a successful login
    # to the CAS server (which returns a 302) will raise an exception.
    # a failed login attempt will not raise any error
    browser.set_handle_robots(False)
    browser.set_handle_redirect(False)

    # open login page
    browser.open(WM_CAS_SERVER_URL)

    # select the login form
    browser.select_form(nr=0)

    # fill in the form with the users email and password
    browser['username'] = email
    browser['password'] = password

    try:
        # submit the form
        browser.submit()
    except HTTPError:
        # if exception is raised, that means a 302 status code
        # was returned, signifing a successful login
        return True

    # failed to login, so user submitted invalid credentials
    return False