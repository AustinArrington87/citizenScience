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
            #resp.message("We are processing your image for SOC!")
      
        # txt metadata
        with open('/Users/austinarrington/citizenScience/sms/img/metadata/'+textFile, 'a') as output:
            output.write(request.values['Body'])
        
    else:
        resp.message("Try sending a picture message/")
    
    filelist = os.listdir(DOWNLOAD_DIRECTORY)
    for file in filelist:
        if file == filename:
            target_file = file
            print("Target File: " + str(target_file))
        else:
            pass
    
    # calculate hue, sat, brightness
    img = cv2.imread('/Users/austinarrington/citizenScience/sms/img/'+str(target_file))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #print(hsv)
    # calculate average color of each row of image
    avg_color_per_row = np.average(hsv, axis=0)
    # calculate the average of rows
    avg_colors = np.average(avg_color_per_row, axis=0)
    
    hue = avg_colors[0]
    sat = avg_colors[1]
    val = avg_colors[2]
    print("Hue: " + str(hue))
    print("Sat: " + str(sat))
    print("Brightness: " + str(val))
    
    SOC = round((0.0781*hue) + 1.74, 2)
    print("SOC (%): " + str(SOC))
    
    resp.message("Soil organic carbon (SOC) analysis complete. SOC (%): " + str(SOC))
    
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)