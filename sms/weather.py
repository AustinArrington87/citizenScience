import requests
import os
import datetime, time
from pysolar.solar import *
from pysolar.radiation import *
import csv

ds_key = os.environ["ds_key"]

#date = datetime.datetime.now(datetime.timezone.utc)
date_time_str = '2020-10-26 20:09:27.243860'
date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')

print("Date Obj: " + str(date_time_obj))
timestamp = int(date_time_obj.timestamp())
print("timestamp: " + str(timestamp))


# get solar angle info 
lat = "40.5833217"
lon = "-87.1281196"

try:
    lat_num = float(lat)
    lon_num = float(lon)
    alt = round(get_altitude(lat_num, lon_num, date_time_obj), 2)
    print("alt: " + str(alt))
    azimuth = round(get_azimuth(lat_num, lon_num, date_time_obj), 2)
    print("azimuth: " + str(azimuth))
    rad = round(radiation.get_radiation_direct(date_time_obj, alt), 2)
    print("radiation: " + str(rad))
except:
    lat_num = None
    lon_num = None
    alt = None
    azimuth = None
    rad = None

try:
    DS_api = "https://api.darksky.net/forecast/"+ds_key+"/"+str(lat)+","+str(lon)+","+str(timestamp)+"?exclude=currently,flags"
    req =  requests.get(DS_api)
    res = req.json()
    cloudCover = res['daily']['data'][0]['cloudCover']
    print("cloudCover: " + str(cloudCover))
    visibility = res['daily']['data'][0]['visibility']
    print("Visibility: " + str(visibility))
    precipProb = res['daily']['data'][0]['precipProbability']
    print("precipProb: " + str(precipProb))
except:
    cloudCover = None
    visibility = None
    precipProb = None
    print("Error with weather call")
    
#        # darksky api call for cloud cover & visibility
#        try:
#            DS_api = "https://api.darksky.net/forecast/"+ds_key+"/"+str(lat)+","+str(lon)+","+str(timestamp)+"?exclude=currently,flags"
#            req =  requests.get(DS_api)
#            res = req.json()
#            #print(res)
#            cloudCover = res['daily']['data'][0]['cloudCover']
#            print("cloudCover: " + str(cloudCover))
#            visibility = res['daily']['data'][0]['visibility']
#            print("Visibility: " + str(visibility))
#        except:
#            cloudCover = None
#            visibility = None
#            print("Darksky api call failed")