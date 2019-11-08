# pip install piexif
# pip install exifread
# pip install GPSPhoto
from GPSPhoto import gpsphoto
data = (gpsphoto.getGPSData('IMG-4115.jpg'))['Latitude']
print(data)
#lat = data['Latitude']
#lon = data['Longitude']
#alt = data['Altitude']
#print(lat)
#print(lon)
#print(alt)


