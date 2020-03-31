import os
from twilio.rest import Client

account_sid = os.environ["account_sid"]
auth_token = os.environ["auth_token"]

client = Client(account_sid, auth_token)

messages = client.messages.list(limit=20)

# SID
for record in messages:
    print(record.sid)
    print(record.body)
    print(record.subresource_uris['media'])