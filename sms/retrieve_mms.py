import os
from twilio.rest import Client
import requests
import json

account_sid = os.environ["account_sid"]
auth_token = os.environ["auth_token"]
BASE_URL = "https://%s:%s@api.twilio.com" % (account_sid, auth_token)

client = Client(account_sid, auth_token)

messages = client.messages.list(limit=20)

# SID
for record in messages:
    print(record.sid)
    print(record.body)
    print(record.subresource_uris['media'])
    print("==============================")
#    sid = record.sid
#    # get media list for each record thtat has one
#    try:
#        message = client.messages(sid).fetch()
#        print(message.body)
#        medias = message.media.list()
#        print(medias)
#        
#        for media in medias:
#            media_instance = client.messages(sid).media(media.sid).fetch()
#            uri = requests.get(BASE_URL + media_instance.uri).json()
#            uri2 = requests.get(BASE_URL + uri['uri'].replace('.json', ''))
#            with open(media_instance.uri.split("/")[-1].replace(".json", ".jpg"), "wb") as f:
#                f.write(uri2.content)
#                f.close()
#    except Exception as e:
#        print(e)