import requests
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

DOWNLOAD_DIRECTORY = '/Users/austinarrington/citizenScience/sms/img'
app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming with message"""
    
    resp = MessagingResponse()
    
    if request.values['NumMedia'] != '0':
        
        # use message SID as file name
        filename = request.values['MessageSid']+'.jpg'
        with open('{}/{}'.format(DOWNLOAD_DIRECTORY, filename), 'wb') as f:
            image_url = request.values['MediaUrl0']
            f.write(requests.get(image_url).content)
            
            resp.message("We are processing your image for SOC!")
    else:
        resp.message("Try sending a picture message/")
    
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)