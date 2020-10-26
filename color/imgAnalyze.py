#  Developed by Austin Arrington
#  Copyright - 2020
import cv2 
import numpy as np 
import csv
import os
from GPSPhoto import gpsphoto
from PIL import Image
import datetime, time
from pysolar.solar import *
from pysolar.radiation import *
import requests

# Darksky weather API key 
ds_key = os.environ["ds_key"]

# Soil organic matter predictor 

def SOM (file):
    som = (0.133*(np.average(np.average(cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2HSV), axis=0), axis=0)[0])) + 2.96
    if som > 10:
        som = 10
    return round(som,4) 

# soil organic carbon predictor 

def SOC (file):
    soc = (0.0772*(np.average(np.average(cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2HSV), axis=0), axis=0)[0])) + 1.72
    if soc > 5.81:
        soc = 5.81
    return round(soc,4)

#image directory 
filelist = os.listdir('/Users/austinarrington/citizenScience/sms/img')
print (filelist)
# now take out file that aren't jpgs 
for file in filelist[:]: # filelist[:] makes a copy of filelist.
    if not(file.endswith(".jpg")):
        filelist.remove(file)
print(filelist)
fileLen = len(filelist)
# loop through and get avg HSV values 

for i, file in enumerate(filelist):
    
    #### hue analyis 
    img = cv2.imread(file)
    # convert rgb to hsv (hue, saturation, value)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #print(hsv) 
    # calculate the average color of each row of our image
    avg_color_per_row = np.average(hsv, axis=0)
    # calculate the averages of our rows
    avg_colors = np.average(avg_color_per_row, axis=0)

    hue = avg_colors[0]
    sat = avg_colors[1]
    val = avg_colors[2]
    print("Hue: " + str(hue))
    print("Saturation: " + str(sat))
    print("Brightness: " + str(val))
    
    # print values to CSV 
    listLen = len(avg_colors)
    #print(listLen)
    file_exists = os.path.isfile('img-hsv.csv')
    with open('img-hsv.csv', 'a') as csvfile:
        headers = ['file', 'hue', 'saturation', 'brightness', 'lat', 'lon', 'alt', 'date', 'make', 'model', 'aperature', 'azimuth', 'radiation', 'cloudCover', 'visibility', 'precipProb', 'som', 'soc']
        writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n', fieldnames=headers)
        if not file_exists:
            writer.writeheader()
            for i, file in enumerate(filelist):
                # GPS coordinates
                coords = gpsphoto.getGPSData(file)
                try:
                    lat = coords['Latitude']
                    lon = coords['Longitude']
                    alt = coords['Altitude']
                except:
                    lat = None
                    lon = None
                    alt = None
                # Extract image metadata
                try:
                    date = Image.open(file)._getexif()[36867]
                    manufacturer = Image.open(file)._getexif()[271]
                    model = Image.open(file)._getexif()[272]
                    aperature = Image.open(file)._getexif()[33437]
                except:
                    date = None
                    manufacturer = None
                    model = None
                    aperature = None
                # solar context metadata
                try:
                    date_obj = datetime.datetime.strptime(date,'%Y:%m:%d %H:%M:%S')
                    date_obj.replace(tzinfo = datetime.timezone.utc)
                    unix_ts = int(date_obj.timestamp())
                except:
                    pass
                #print(unix_ts)
                try:
                    azimuth = round(get_azimuth(lat, lon, date_obj), 2)
                    rad = round(radiation.get_radiation_direct(date_obj, alt), 2)
                except:
                    azimuth = None
                    rad = None
                # Weather context data 
                try:
                    DS_api = "https://api.darksky.net/forecast/"+ds_key+"/"+str(lat)+","+str(lon)+","+str(unix_ts)+"?exclude=currently,flags"
                    req = requests.get(DS_api)
                    res = req.json()
                    #print(res)
                    cloudCover = res['daily']['data'][0]['cloudCover']
                    visibility = res['daily']['data'][0]['visibility']
                    precipProb = res['daily']['data'][0]['precipProbability']
                except:
                    cloudCover = None
                    visibility = None
                    precipProb = None
                    print("Error with weather API call")
                        
                writer.writerow({
                    'file': file,
                    'hue': np.average(np.average(cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2HSV), axis=0), axis=0)[0],
                    'saturation': np.average(np.average(cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2HSV), axis=0), axis=0)[1],
                    'brightness': np.average(np.average(cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2HSV), axis=0), axis=0)[2],
                    'lat': lat,
                    'lon': lon,
                    'alt': alt,
                    'date': date,
                    'make': manufacturer,
                    'model': model,
                    'aperature': aperature,
                    'azimuth': azimuth,
                    'radiation': rad,
                    'cloudCover': cloudCover,
                    'visibility': visibility,
                    'precipProb': precipProb,
                    'som': SOM(file),
                    'soc': SOC(file)
                    })
                 