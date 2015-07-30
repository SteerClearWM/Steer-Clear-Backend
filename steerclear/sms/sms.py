import twilio

class SteerClearTwilioClient(twilio.rest.TwilioRestClient):

    def __init__(self, account_sid, auth_token, twilio_number):
        super(SteerClearTwilioClient, self).__init__(account_sid, auth_token)
        self.twilio_number = twilio_number

    def notify_user(self, user_number, message):
        try:
            message = self.messages.create(
                body=message,
                to=user_number,
                from_=self.twilio_number
            )
        except twilio.TwilioRestException as e:
            print e
            return None
        return message