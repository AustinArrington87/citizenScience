import requests
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import os
import cv2
import numpy as np
import datetime, time
from pysolar.solar import *
from pysolar.radiation import *
import csv
from PIL import Image

# documentation: https://www.twilio.com/docs/sms/twiml

DOWNLOAD_DIRECTORY = '/Users/austinarrington/citizenScience/sms/img'
META_DIRECTORY = '/Users/austinarrington/citizenScience/sms/img/metadata'
# darksky
ds_key = os.environ["ds_key"]

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
        textLines = textBody.split()
        try:
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
            lat = None
            lon = None
            print("Can't parse lat/lon from metadata")
        # get lab ID
        try:
            labID = textLines[2]
        except:
            labID = None
            print("Can't find LabID")
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
            lat_num = None
            lon_num = None
            alt = None
            azimuth = None
            rad = None
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
            cloudCover = None
            visibility = None
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
        try:
            with open('/Users/austinarrington/citizenScience/sms/img/light_data/'+textFile, 'a') as output:
                output.write('{}\n{}\n{}\n{}\n{}\n'.format(str(alt),str(azimuth),str(rad),str(cloudCover),str(visibility)))
        except:
            print("Could not collect light context data, no valid coordinates passed...")
            
        
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
    
    # img metadata
    #dateCam = Image.open(labID+'.jpg')._getexif()[36867]
    #manufacturer = Image.open(labID+'.jpg')._getexif()[271]
    
    # soil organic matter
#    SOM = round((0.133*hue) + 2.96, 2)
#    if SOM > 10:
#        SOM = 10
#    # soil organic carbon
#    SOC = round((0.0772*hue) + 1.72, 2)
#    if SOC > 5.8:
#        SOC = 5.8
#    print("SOM (%): " + str(SOM))
#    print("SOC (%): " + str(SOC))
    
    # Step 1: Calculate Percent Clay 
    clayPercent = round((-0.0853*sat)+37.1,2)
    # Step 2: Estimate SOC % 
    SOC = round((0.05262*hue) + (0.11041*clayPercent) + -2.76983,2)
    # Step 3: Convert SOC % to SOM %
    SOM = round(SOC*1.72,2)
    # Step 4: Estimate Bulk Density (g/cm3)
    bulkDensity = round((0.0129651*clayPercent) + (0.0030006*sat) + 0.4401499,2)
    # Step 5: Convert SOC % to SOC (t/ha)
    # assume 6in as depth 
    depth_cm = 6*2.54
    SOC_vol = round((SOC*0.01)*(bulkDensity*(depth_cm/100)*10000),2)
    
    # write everything to CSV
    try:
        file_exists = os.path.isfile('soc.csv')
        with open('soc.csv', 'a') as csvfile:
            headers = ['id', 'time', 'lat', 'lon', 'h', 's', 'v', 'alt', 'az', 'rad', 'cc', 'vis', 'som', 'soc', 'bd', 'soc_tha', 'clay']
            writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n', fieldnames=headers)
            if not file_exists:
                writer.writeheader()
                writer.writerow({
                    'id': labID,
                    'time': timestamp,
                    'lat': lat,
                    'lon': lon,
                    'h': hue,
                    's': sat,
                    'v': val,
                    'alt': alt,
                    'az': azimuth,
                    'rad': rad,
                    'cc': cloudCover,
                    'vis': visibility,
                    'som': SOM,
                    'soc': SOC,
                    'bd': bulkDensity,
                    'soc_tha': SOC_vol,
                    'clay': clayPercent
                })
            if file_exists:
                writer.writerow({
                    'id': labID,
                    'time': timestamp,
                    'lat': lat,
                    'lon': lon,
                    'h': hue,
                    's': sat,
                    'v': val,
                    'alt': alt,
                    'az': azimuth,
                    'rad': rad,
                    'cc': cloudCover,
                    'vis': visibility,
                    'som': SOM,
                    'soc': SOC,
                    'bd': bulkDensity,
                    'soc_tha': SOC_vol,
                    'clay': clayPercent
                })
    except:
        pass
    
    resp.message("Soil organic matter (SOM) and soil organic carbon (SOC) analysis complete.\n SOM (%): " + str(SOM) + "\n SOC (%): " + str(SOC) + "\n BD (g/cm3): " + str(bulkDensity) + "\n SOC (t/ha): " + str(SOC_vol))
    
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)