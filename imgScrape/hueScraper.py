# Citizen Science Open Source Code Project 
import flickrapi
import urllib.request
from PIL import Image
import csv
import os
import numpy as np 
import cv2 
# enter flickr API key and secret
# create API Key here: https://www.flickr.com/services/apps/create/apply
api_key = 'ENTER api_key'
api_secret = 'ENTER api_secret'
flickr=flickrapi.FlickrAPI(api_key, api_secret, cache=True)

# filter search by keyword to further limit scope of query 
keyword = 'squirrel'

# set cutoff point for image query
queryCutoff = 5 

# NOTES: provide min_upload_date in UNIX timstamp, everything after is returned 
# bbox = A comma-delimited list of 4 values defining the Bounding Box of the area that will be searched. The 4 values represent the bottom-left corner of the box and the top-right corner, minimum_longitude, minimum_latitude, maximum_longitude, maximum_latitude.

# min_upload_date == 01/01/2001
# bbox in this example is for Central Park

photos = flickr.walk(
                     text=keyword,
                     tag_mode='all',
                     tags=keyword,
                     min_upload_date = 978325200,
                     bbox = "-73.98171,40.76837,-73.94969,40.79656",
                     extras='url_c,geo,date_taken',
                     per_page=100,           
                     sort='relevance'
                    )

urls = []
for i, photo in enumerate(photos):
    #print (i)
    url = photo.get('url_c')
    urls.append(url)
    
    if i > queryCutoff:
        break
        
print (urls)
###############################
###############################
# download and resize photos to working directory 
responseLen = len(urls)
for i in range(0,responseLen):
    try:
        urllib.request.urlretrieve(urls[i], str(i)+'.jpg')
        Image.open(str(i)+'.jpg').resize((256, 256), Image.ANTIALIAS).save(str(i)+'.jpg')
    except:
        pass
    
# QUERY IMAGE METADATA 
imageIDs = []       
latitudes = []
longitudes = []
dates = []

for i, url in enumerate(photos):   
    #image ID 
    imageID = url.attrib['id']
    imageIDs.append(imageID)
    
    #datetaken
    datetaken = url.attrib['datetaken']
    dates.append(datetaken)
    
    # latitude 
    latitude = url.attrib['latitude']
    latitudes.append(latitude)
    #longitude 
    longitude = url.attrib['longitude']
    longitudes.append(longitude)
        
    #csv parameters 
    file_exists = os.path.isfile('img-metadata.csv')
    with open('img-metadata.csv', 'a') as csvfile:
        headers = ['id', 'url', 'datetaken', 'imgName', 'latitude', 'longitude']
        writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n', fieldnames=headers)
        if not file_exists:
            writer.writeheader()
            for i, url in enumerate(photos):
                writer.writerow({
                    'id': url.attrib['id'],
                    'url': 'http://flickr.com/photo.gne?id='+str(url.attrib['id']),
                    'datetaken': url.attrib['datetaken'],
                    'imgName': str(i)+'.jpg', 
                    'latitude': url.attrib['latitude'],
                    'longitude': url.attrib['longitude']
                })
                if i > queryCutoff:
                    break
    # break the loop
    if i > queryCutoff:
        break

### now get Hue, Saturation, Brightness values and save to separate CSV 

# working directory with files 
filelist = os.listdir('/Users/austinarrington/citizenScience/imgScrape')
print (filelist)
# now take out file that aren't jpgs 
for file in filelist[:]: # filelist[:] makes a copy of filelist.
    if not(file.endswith(".jpg")):
        filelist.remove(file)
print(filelist)
fileLen = len(filelist)
# loop through and get avg HSV values 

for i, file in enumerate(filelist):
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
        headers = ['file', 'hue', 'saturation', 'brightness']
        writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n', fieldnames=headers)
        if not file_exists:
            writer.writeheader()
            for i, file in enumerate(filelist):
                writer.writerow({
                    'file': file,
                    'hue': np.average(np.average(cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2HSV), axis=0), axis=0)[0],
                    'saturation': np.average(np.average(cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2HSV), axis=0), axis=0)[1],
                    'brightness': np.average(np.average(cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2HSV), axis=0), axis=0)[2]
                    })
                 
    
