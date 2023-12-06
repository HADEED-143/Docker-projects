from django.http import HttpResponse
from twilio.rest import Client
import os # for environment variables


def send_sms(request, body, to):
    # Your Twilio Account SID and Auth Token
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    number = os.environ['TWILIO_NUMBER'] 

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=body,
        from_=number,  # Your Twilio phone number
        to=to  # The phone number you want to send the SMS to
    )

    return HttpResponse('SMS sent!', status=200)


# Constants
ROLE_CHOICES = (
    ('client', 'client'),
    ('worker', 'worker'),
    ('contractor', 'contractor'),
    ('superuser', 'superuser'),
)

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
)

JOB_TYPES = (
    ('on-site', 'On-site'),
    ('remote', 'Remote')
)

BID_STATUS = (
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
    ('completed', 'Completed'),
    ('in-progress', 'In-progress'),
)

JOB_STATUS = (
    ('open', 'Open'),
    ('closed', 'Closed'),
    ('in-progress', 'In-progress'),
    ('paused', 'Paused'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
)

