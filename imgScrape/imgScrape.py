# Written by Austin Arrington 
# 10.16.18 

import flickrapi
import urllib.request
from PIL import Image
# enter flickr API key and secret
flickr=flickrapi.FlickrAPI('api_key', 'api_secret', cache=True)

# search by keyword 
#keyword = 'siberian husky'

# NOTES: provide min_upload_date in UNIX timstamp, everything after is returned 
# bbox = A comma-delimited list of 4 values defining the Bounding Box of the area that will be searched. The 4 values represent the bottom-left corner of the box and the top-right corner, minimum_longitude, minimum_latitude, maximum_longitude, maximum_latitude.

photos = flickr.walk(
                     #text=keyword,
                     #tag_mode='all',
                     #tags=keyword,
                     min_upload_date = 1538361059,
                     bbox = "-122.42307100000001,37.773779,-122.381071,37.815779",
                     extras='url_c',
                     per_page=100,           # may be you can try different numbers..
                     sort='relevance')

urls = []
for i, photo in enumerate(photos):
    print (i)
    
    url = photo.get('url_c')
    urls.append(url)
    
    # get 50 urls
    if i > 50:
        break

#print (urls)

responseLen = len(urls)

for i in range(0,responseLen):
    urllib.request.urlretrieve(urls[i], 'img'+str(i)+'.jpg')
    Image.open('img'+str(i)+'.jpg').resize((256, 256), Image.ANTIALIAS).save('img'+str(i)+'.jpg')
    # resize image 
    
