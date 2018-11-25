# Mini_Proj_3
## About the Project 
This is the third mini project. The goal of this project was to expand on mini project 1 and add two different databases to it. This project adds MongoDB and MySQL through additional API calls. 

# How To Run
1) cd into the directory you downloaded the files to. 
2) Update the "twitter_globals_secret.py" file with your own credentials.
3) Update the JSON path in Main.py to point to your Google API credentials.
4) Run: "python Main.py" or "pyhton3 Main.py"

The program will ask for a Twitter handle. It will fetch the images and store them in ./img/<twitter_handle>.
Then it will concatenate then images into a video. 
It will atempt to analyze the video. If it does a file video_descriptions.txt will be in the ./img/<twitter_handle> directory.
If it cannot process the video it will try and annotate each image. Those results will be in image_descriptions.txt, also in the ./img/<twitter_handle> directory.

# Setup
## For the Mini-Project 1 portion:
### Python 3
You need to run the program with Python 3. My OS is MAC OS 10.13.6, and it natively has Python 2.8 installed. I installed Python 3 separately (see: https://www.python.org/downloads/).

Once that is installed you need to install the APIs 
### Tweepy
Visit: http://www.tweepy.org for more information.


### ffmpy
Visit: https://ffmpy.readthedocs.io/en/latest/index.html for more information.

### Google API
Visit: https://cloud.google.com/vision/?utm_source=google&utm_medium=cpc&utm_campaign=na-US-all-en-dr-bkws-all-all-trial-p-dr-1003905&utm_content=text-ad-none-any-DEV_c-CRE_291204483525-ADGP_Hybrid+%7C+AW+SEM+%7C+BKWS+%7C+US+%7C+en+%7C+PHR+%7E+ML%2FAI+%7E+Vision+API+%7E+Google+Vision+Api-KWID_43700036550340461-kwd-475191349900&utm_term=KW_google%20vision%20api-ST_Google+Vision+Api&gclid=Cj0KCQjwof3cBRD9ARIsAP8x70MrbWuagu5kUI8Ku20lO90M3ll8gwYEoPO-y7Uv2t6X6e_-pQFmzX0aAlNNEALw_wcB&dclid=CKT38Kuww90CFc5lwQodVN4Ceg

### Needed accounts
You will need a Twitter developer account and a Consumer Key and Secret, and an Access Token and Secret. I have not provided those as it would compromise my information. 

Once you have the keys you can replace empty place holders in "twitter_globals_secret.py" with your valid values.

You will need a Google Developer account. You need to enable The Cloud Vision API and the Video Intelligence API. You need to set up billing for this to work. Download the JSON credentials. 

## For the Mini-Project 3 portion:
### Install MySQL locally
1) For Mac OS install MySQL using this guide: https://dev.mysql.com/doc/refman/5.7/en/osx-installation-pkg.html 
### Set up the database and tables
1) Update the username and passwords in the file "sqlConnectInfo.py" with the password and username you used when installing MySQL. Update the HOST in the file MySQL_Helper.py and MySQL_setup.py if you are not using localhost for your MySQL instance.
2) Run the provided MySQL_setup.py file. This script will create the required databases and tables needed by the project
### Install Mongo DB Locally
I am running on Mac OS. The following steps are the ones I used to install it on my computer.

https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/#install-mongodb-community-edition

You must run Mongo DB locally before you can use the API. Once it is installed you can runn the command "mongod".


