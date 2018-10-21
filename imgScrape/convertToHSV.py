# Citizen Science Open Source Code Project 
import flickrapi
import urllib.request
from PIL import Image
import colorsys
import csv
import os

def HSVColor(img):
    if isinstance(img,Image.Image):
        r,g,b = img.split()
        Hdat = []
        Sdat = []
        Vdat = [] 
        for rd,gn,bl in zip(r.getdata(),g.getdata(),b.getdata()) :
            h,s,v = colorsys.rgb_to_hsv(rd/255.,gn/255.,bl/255.)
            Hdat.append(int(h*255.))
            Sdat.append(int(s*255.))
            Vdat.append(int(v*255.))
        r.putdata(Hdat)
        g.putdata(Sdat)
        b.putdata(Vdat)
        print("Red: " + str(rd))
        print("Green: " + str(gn))
        print("Blue: " + str(bl))
        print("Hue: " + str(h))
        print("Saturation: " + str(s))
        print("Value: " + str(v))
        return Image.merge('RGB',(r,g,b))
    else:
        return None
# working directory with files 
filelist = os.listdir('/Users/austinarrington/citizenScience/imgScrape')
print (filelist)
# now take out file that aren't jpgs 
for fichier in filelist[:]: # filelist[:] makes a copy of filelist.
    if not(fichier.endswith(".jpg")):
        filelist.remove(fichier)
print(filelist)

# now do our HSV value conversions 

for file in filelist:
    #HSVColor(Image.open(file)
    HSVColor(Image.open(file)).save('HSV_'+str(file))
    
       

