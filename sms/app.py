import requests
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import os
import cv2
import numpy as np
import datetime, time
from pysolar.solar import *
from pysolar.radiation import *

# documentation: https://www.twilio.com/docs/sms/twiml
# https://www.twilio.com/blog/2018/05/how-to-receive-and-download-picture-messages-in-python-with-twilio-mms.html

DOWNLOAD_DIRECTORY = '/Users/austinarrington/citizenScience/sms/img'
META_DIRECTORY = '/Users/austinarrington/citizenScience/sms/img/metadata'
# darksky
ds_key = os.environ["ds_key"]
#ds_key = os.environ["4220aeb6ebb11c7abd00a31ae35cab06"]

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
        # parse txt file for lat lon
        try:
            textLines = textBody.split()
            lat = textLines[0]
            try:
                lat = lat.rstrip(',')
            except:
                lat = lat
            lon = textLines[1]
            if lat != None:
                print("Lat: " + str(lat))
            if lon != None:
                print("Lon: " + str(lon))
        except:
            print("Can't parse lat/lon from metadata")
        # get current time 
        date = datetime.datetime.now(datetime.timezone.utc)
        print("date: " + str(date))
        timestamp = int(date.timestamp())
        print("timestamp: " + str(timestamp))
        # get solar angle info
        try:
            lat_num = float(lat)
            lon_num = float(lon)
            alt = round(get_altitude(lat_num, lon_num, date), 2)
            print("alt: " + str(alt))
            azimuth = round(get_azimuth(lat_num, lon_num, date), 2)
            print("azimuth: " + str(azimuth))
            rad = round(radiation.get_radiation_direct(date, alt), 2)
            print("radiation: " + str(rad))
        except:
            print("Can't get solar angle info...")
        # darksky api call for cloud cover & visibility
        try:
            DS_api = "https://api.darksky.net/forecast/"+ds_key+"/"+str(lat)+","+str(lon)+","+str(timestamp)+"?exclude=currently,flags"
            req =  requests.get(DS_api)
            res = req.json()
            #print(res)
            cloudCover = res['daily']['data'][0]['cloudCover']
            print("cloudCover: " + str(cloudCover))
            visibility = res['daily']['data'][0]['visibility']
            print("Visibility: " + str(visibility))
        except:
            print("Darksky api call failed")
        
        # save image file to local directory 
        with open('{}/{}'.format(DOWNLOAD_DIRECTORY, filename), 'wb') as f:
            image_url = request.values['MediaUrl0']
            f.write(requests.get(image_url).content)
            #resp.message("We are processing your image for SOC!")
      
        # SMS txt metadata
        with open('/Users/austinarrington/citizenScience/sms/img/metadata/'+textFile, 'a') as output:
            output.write(request.values['Body'])
        
        # save light context data
        with open('/Users/austinarrington/citizenScience/sms/img/light_data/'+textFile, 'a') as output:
            output.write('{}\n{}\n'.format(str(cloudCover),str(visibility)))
            
        
    else:
        resp.message("Please resend your image. Email info@plantgroup.co for customer support.")
    
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