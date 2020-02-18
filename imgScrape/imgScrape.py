# Citizen Science Open Source Code Project 
import flickrapi
import urllib.request
from PIL import Image
import csv
import os
# enter flickr API key and secret
# create API Key here: https://www.flickr.com/services/apps/create/apply
api_key = 'ENTER api_key'
api_secret = 'ENTER api_secret'
flickr=flickrapi.FlickrAPI(api_key, api_secret, cache=True)

# filter search by keyword to further limit scope of query 
keyword = 'solar'

# set cutoff point for image query
queryCutoff = 200 

# NOTES: provide min_upload_date in UNIX timstamp, everything after is returned 
# bbox = A comma-delimited list of 4 values defining the Bounding Box of the area that will be searched. The 4 values represent the bottom-left corner of the box and the top-right corner, minimum_longitude, minimum_latitude, maximum_longitude, maximum_latitude.

# min_upload_date == 01/01/2001
# bbox in this example is for Central Park

photos = flickr.walk(
                     text=keyword,
                     tag_mode='all',
                     tags=keyword,
                     min_upload_date = 978325200,
                     bbox = "-156.05277778,19.07097778,-154.76694444,19.76135556",
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
#
#

    
