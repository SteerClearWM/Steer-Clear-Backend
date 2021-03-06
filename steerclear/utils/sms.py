import twilio

"""
SteerClearSMSClient
----------------------
Subclass of TwilioRestClient allowing for a simple interface
to interact with the twilio api while still remaining decoupled
from the Flask app
"""
class SteerClearSMSClient(twilio.rest.TwilioRestClient):

    """
    __init__
    --------
    Create new SteerClearSMSClient instance. calls super classes'
    __init__() method, passing in the account_sid and auth_token and
    saves the passed in twilio_number
    """
    def __init__(self, account_sid, auth_token, twilio_number):
        super(SteerClearSMSClient, self).__init__(account_sid, auth_token)
        self.my_number = twilio_number

    """
    notify_user
    -----------
    Send a message to the specified users phone. On success,
    returns the message object. On failure, print exception and return
    None for now.
    """
    def notify_user(self, user_number, message):
        try:
            message = self.messages.create(
                body=message,
                to=user_number,
                from_=self.my_number
            )
        except twilio.TwilioRestException as e:
            print e
            return None
        return message