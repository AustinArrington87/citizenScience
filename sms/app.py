import requests
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import os
import cv2
import numpy as np

# documentation: https://www.twilio.com/docs/sms/twiml

DOWNLOAD_DIRECTORY = '/Users/austinarrington/citizenScience/sms/img'
META_DIRECTORY = '/Users/austinarrington/citizenScience/sms/img/metadata'

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming with message"""
    
    resp = MessagingResponse()
    
    if request.values['NumMedia'] != '0':
        
        # use message SID as file name
        filename = request.values['MessageSid']+'.jpg'
        textBody = request.values['Body']
        textFile = request.values['MessageSid']+'.txt'
        print(filename)
        print(textBody)
        with open('{}/{}'.format(DOWNLOAD_DIRECTORY, filename), 'wb') as f:
            image_url = request.values['MediaUrl0']
            f.write(requests.get(image_url).content)
            
            resp.message("We are processing your image for SOC!")
        
        # txt metadata
        with open('/Users/austinarrington/citizenScience/sms/img/metadata/'+textFile, 'a') as output:
            output.write(request.values['Body'])
        
    else:
        resp.message("Try sending a picture message/")
    
     # now send prediction
    filelist = os.listdir(DOWNLOAD_DIRECTORY)
    #print(filelist)
    fileLen = len(filelist)
    # get hsv values
    for i, file in enumerate(filelist):
        #print(file)
        if file == filename:
            print(file)
            img = cv2.imread(file,1)
            print(img)
    
    
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)