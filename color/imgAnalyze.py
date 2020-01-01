#  Developed by Austin Arrington
#  Copyright - 2019
import cv2 
import numpy as np 
import csv
import os
from GPSPhoto import gpsphoto
from PIL import Image

# working directory with files 
filelist = os.listdir('/Users/austinarrington/citizenScience/color')
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
        headers = ['file', 'hue', 'saturation', 'brightness', 'lat', 'lon', 'alt', 'date']
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
                # Date
                try:
                    date = Image.open(file)._getexif()[36867]
                except:
                    date = None
                writer.writerow({
                    'file': file,
                    'hue': np.average(np.average(cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2HSV), axis=0), axis=0)[0],
                    'saturation': np.average(np.average(cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2HSV), axis=0), axis=0)[1],
                    'brightness': np.average(np.average(cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2HSV), axis=0), axis=0)[2],
                    'lat': lat,
                    'lon': lon,
                    'alt': alt,
                    'date': date
                    })
                 