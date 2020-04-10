from pysolar.solar import *
from pysolar.radiation import *
import datetime, time
import requests
import os

# outdoor color normalization can be addressed through context - sun angle &  cloud cover
# https://www.cs.colostate.edu/pubserv/pubs/Buluswar-draper-publications-buluswar_cviu02.pdf

# darksky api key
ds_key = os.environ["ds_key"]
print("DS: " + ds_key)

#latitude = 39.7391536
#longitude = -104.9847034

latitude = 38.9029278
longitude = -76.885033

#date = datetime.datetime.now()
# current_time = datetime.datetime.now(datetime.timezone.utc)
# yr, month, day, hour, sec, microsec
#date = datetime.datetime(2007, 2, 18, 15, 13, 1, 130320, tzinfo=datetime.timezone.utc)
date = datetime.datetime(2019, 11, 11, 14, 58, 22, tzinfo=datetime.timezone.utc)
print("Date: " + str(date))
# also get UNIX timestamp for Darsky
timestamp = int(date.timestamp())
print("timestamp: " + str(timestamp))
# calculate angle between sun and plane tangent to where you are
alt = round(get_altitude(latitude, longitude, date), 2)
print("altitude: " + str(alt))
#  calculate azimuth of sun
azimuth = round(get_azimuth(latitude, longitude, date), 2)
print("azimuth: " + str(azimuth))
# now calculate dirrect radiation (clear-sky) from the sun
rad = round(radiation.get_radiation_direct(date, alt), 2)
print("radiation: " + str(rad))

# calculate cloud cover
DS_api = "https://api.darksky.net/forecast/"+ds_key+"/"+str(latitude)+","+str(longitude)+","+str(timestamp)+"?exclude=currently,flags"

req =  requests.get(DS_api)
res = req.json()
#dataLoad = res['daily']['data'][0]
#print(dataLoad)
cloudCover = res['daily']['data'][0]['cloudCover']
print("cloudCover: " + str(cloudCover))
visibility = res['daily']['data'][0]['visibility']
print("Visibility: " + str(visibility))
