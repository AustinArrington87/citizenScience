from twilio.rest import Client
import os

account_sid = os.environ["account_sid"]
auth_token = os.environ["auth_token"]

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+18144047040",
    from_="+17174475615",
    body="This is the ship that made the Kessel Run in fourteen parsecs?",
    media_url=["https://c1.staticflickr.com/3/2899/14341091933_1e92e62d12_b.jpg"])

print(message.sid)
print(message.status)
print(message.media._uri)