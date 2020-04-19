# Selenium WebDriver drives a browser natively, as a real user would, either locally or on remote machines.
# https://www.selenium.dev/projects/
# https://chromedriver.chromium.org/downloads  --> if using Chrome, download this web driver and save to your directory of choice

from selenium import webdriver
import time
import urllib.request
import os
from selenium.webdriver.common.keys import Keys
import csv


# convert species name CSV row as numpy array 

def imgDownload(key_words):   
    browser = webdriver.Chrome("/Users/austinarrington/chromedriver")
    browser.get("https://www.google.com/")

    search = browser.find_element_by_name('q')

    #key_words = "Anisocampium niponicum"
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

    # rename image to species name 
    dst = '/Users/austinarrington/citizenScience/imgScrape/downloads/'+key_words+'.jpg'
    src = '/Users/austinarrington/citizenScience/imgScrape/downloads/'+'image5.jpg'
    os.rename(src, dst)
    # close browser
    browser.close()


speciesName = []
with open('PlantFinder.csv', mode='r') as f:
    reader = csv.reader(f, delimiter=',')
    for n, row in enumerate(reader):
        if not n: #skip header
            continue
        speciesName.append(row[1])

print("Done importing species names...")
for name in speciesName:
    print(name)
    imgDownload(name)

