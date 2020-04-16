#  https://medium.com/@reddy.incognito/download-images-from-google-using-python-20d6588fc3f1

# Selenium WebDriver drives a browser natively, as a real user would, either locally or on remote machines.

# https://www.selenium.dev/projects/
# https://chromedriver.chromium.org/downloads  --> if using Chrome, download this web driver and save to your directory of choice

from selenium import webdriver
import time
import urllib.request
import os
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome("/Users/austinarrington/chromedriver")
browser.get("https://www.google.com/")

search = browser.find_element_by_name('q')


# get search bar field from Google
key_words = "Anisocampium niponicum"
search.send_keys(key_words,Keys.ENTER)
# click on Images page
elem = browser.find_element_by_link_text('Images')
elem.get_attribute('href')
elem.click()

#comment out for teting
sub = browser.find_elements_by_tag_name("img")
# create folder  for downloads  
try:
    os.mkdir('downloads')
except FileExistsError:
    pass

# extract random image -- just make sure it's not 1.jpg (Google Logo)

# subsample of results 
for i in sub[1:10]:
    src = i.get_attribute('src')
    try:
        if src != None:
            src = str(src)
            print(src)
            urllib.request.urlretrieve(src, os.path.join('downloads','image'+str(5)+'.jpg'))
            # rename img name to species name
        else:
            raise TypeError
    except TypeError:
        print('Fail')
    








