# citizenScience
Python scripts for citizen science projects involving data mining and image analysis. 

imgScrape/imgScrape.py scrapes images from the Flickr API using bounding box, keyword, time and other filter parameters. Images are saved to the users working directory and a CSV is output with image metadata. 

hueScraper.py scrapes images and then converts all images into Hue Sturation Brightness values. 

These scripts can be utilized for mining and analyzing images of the natural world through citizen science. Have fun! 

color/correction:   uses Darksky and pysolar to find context (sun angle + cloud cover) for color normilization of outdoor photos

SMS 

The sms folder holds a Django web app for processing mms / sms data from Twilio. This functionality is used for processing img data sent from the field to our Twilio number. 

Twilio documentation: 
https://www.twilio.com/docs/sms/twiml
https://www.twilio.com/blog/2018/05/how-to-receive-and-download-picture-messages-in-python-with-twilio-mms.html

1. Clone repo 

$ git clone https://github.com/AustinArrington87/citizenScience.git

2. Install dependencies
$ pip install flask
$ pip install requests
$ pip install twilio


3. Update directory path in app.py

4. For testing on local ownload ngrok https://ngrok.com/download and drag the zipped folder into sms subdirectory
$ unzip /path/to/ngrok.zip
$ ./ngrok authtoken <YOUR_AUTH_TOKEN>

5. Run the web app 
$ cd citizenScience/sms
$ python app.py
$ ./ngrok http 5000

6. Configure Twilo
- Purchase phone number on Twilio
- Go to Phone Numbers / Manage Numbers / Active Numbers
- Click on your phone number, takes you to "Configue". Scrol to bottom of page to Messaging section
- In "a message comes in section" change dropdown field to "Webhook", pasted in your ngrok url with /sms added (like this: http://xxxxxxxxngrok.io/sms) (HTTP POST)
- Save changes. Text an image to your number. You will get a confirmation message and find the image in /sms/img folder! 



