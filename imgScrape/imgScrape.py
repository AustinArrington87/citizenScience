# Citizen Science Open Source Code Project 
import flickrapi
import urllib.request
from PIL import Image
# enter flickr API key and secret
api_key = '<enter api_key>'
api_secret = '<enter api_secret>'
flickr=flickrapi.FlickrAPI(api_key, api_secret, cache=True)

# filter search by keyword to further limit scope of query 
keyword = 'tree'

# set cutoff point for image query
# the loop breaks if i > queryCutoff, so by setting to 3 - 5 photos are queried (as 0 is first index)
queryCutoff = 3 

# NOTES: provide min_upload_date in UNIX timstamp, everything after is returned 
# bbox = A comma-delimited list of 4 values defining the Bounding Box of the area that will be searched. The 4 values represent the bottom-left corner of the box and the top-right corner, minimum_longitude, minimum_latitude, maximum_longitude, maximum_latitude.

photos = flickr.walk(
                     #text=keyword,
                     #tag_mode='all',
                     #tags=keyword,
                     min_upload_date = 1538361059,
                     bbox = "-122.42307100000001,37.773779,-122.381071,37.815779",
                     extras='url_c,geo',
                     per_page=100,           
                     sort='relevance')

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
    urllib.request.urlretrieve(urls[i], 'img'+str(i)+'.jpg')
    Image.open('img'+str(i)+'.jpg').resize((256, 256), Image.ANTIALIAS).save('img'+str(i)+'.jpg')

# QUERY IMAGE METADATA 
imageIDs = []       
latitudes = []
longitudes = []
for i, url in enumerate(photos):
    #image ID 
    imageID = url.attrib['id']
    imageIDs.append(imageID)
    # latitude 
    latitude = url.attrib['latitude']
    latitudes.append(latitude)
    #longitude 
    longitude = url.attrib['longitude']
    longitudes.append(longitude)
    if i > queryCutoff:
        break
print(imageIDs)
print(latitudes)
print(longitudes)
    
