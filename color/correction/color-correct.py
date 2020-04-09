from pysolar.solar import *
from pysolar.radiation import *
import datetime, time
import requests
import os

# darksky api key
ds_key = os.environ["ds_key"]
print("DS: " + ds_key)

latitude = 39.7391536
longitude = -104.9847034

date = datetime.datetime.now()
# current_time = datetime.datetime.now(datetime.timezone.utc)
print("Date: " + str(date))
# yr, month, day, hour, sec, microsec
# date = datetime.datetime(2007, 2, 18, 15, 13, 1, 130320, tzinfo=datetime.timezone.utc)
# also get UNIX timestamp for Darsky
timestamp = int(date.timestamp())
print("timestamp: " + str(timestamp))
# calculate angle between sun and plane tangent to where you are
alt = get_altitude(latitude, longitude, date)
print("altitude: " + str(alt))
#  calculate azimuth of sun
azimuth = get_azimuth(latitude, longitude, date)
print("azimuth: " + str(azimuth))
# now calculate dirrect radiation (clear-sky) from the sun
rad = radiation.get_radiation_direct(date, alt)
print("radiation: " + str(rad))

# calculate cloud cover
DS_api = "https://api.darksky.net/forecast/"+ds_key+"/"+str(latitude)+","+str(longitude)+","+str(timestamp)+"?exclude=currently,flags"

req =  requests.get(DS_api)
res = req.json()
cloudCover = res['daily']['data'][0]['cloudCover']
print(cloudCover)

