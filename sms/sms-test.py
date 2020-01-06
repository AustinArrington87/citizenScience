from twilio.rest import Client
import os

account_sid = os.environ["account_sid"]
auth_token = os.environ["auth_token"]

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+18144047040",
    from_="+17174475615",
    body="Hello from Python!")

"""
multiple numbers

numbers_to_message = ['+15558675310', '+14158141829', '+15017122661']
for number in numbers_to_message:
    client.messages.create(
        body = 'Hello from my Twilio number!',
        from_ = '+17174475615',
        to = 'number'
    )
"""

print(message.sid)
print(message.status)