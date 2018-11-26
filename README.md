# Mini_Proj_3
## About the Project 
This is the third mini project. The goal of this project was to expand on mini project 1 and add two different databases to it. This project adds MongoDB and MySQL through additional API calls. To view mini project 1 visit: https://github.com/zorzonp/BU_API_Project

# New APIs
## MySQL
This API provides the functions to connect to a local instance of MySQL and create a database.
This API also provides the functions to create the tables needed by the main project to store transactions and information about labels.


## Mongo DB
This API provides the functions to connect to a local instnce of MongoDB and to create a database and collections. 
This API also provides functions to add transactions to the proper collection and label info to their collection.

# How To Run
1) cd into the directory you downloaded the files to. 
2) Update the "twitter_globals_secret.py" file with your own credentials.
3) Update the JSON path in Main.py to point to your Google API credentials.
4) Update the "sqlConnectInfo.py" file with the correct credentials you used when setting up your local MySQL instance.**
5) Update the "HOST" variabe in "MySQL_Helper.py" if you are not using local host.**
6) Run: "python 3.5 Main.py"

** denote new steps related to the MySQL and MongoDB APIs

The program will ask for a Twitter handle. It will fetch the images and store them in ./img/<twitter_handle>. It will record the transactions in the two databases. It will then annotate each image and add the results to the databases. Those results will also be in "image_descriptions.txt", also in the ./img/<twitter_handle> directory.
Then it will concatenate then images into a video. 


# Setup
## For the Mini-Project 1 portion:
### Python 3
You need to run the program with Python 3.5. My OS is MAC OS 10.13.6, and it natively has Python 2.8 installed. I installed Python 3.5 separately (see: https://www.python.org/downloads/).

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
1) Update the username and passwords in the file "sqlConnectInfo.py" with the password and username you used when installing MySQL. Update the HOST in the file MySQL_Helper.py if you are not using localhost for your MySQL instance.

### Install Mongo DB Locally
I am running on Mac OS. The following steps are the ones I used to install it on my computer.

https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/#install-mongodb-community-edition

You must run Mongo DB locally before you can use the API. Once it is installed you can run the command "mongod" to start Mongo DB.

Once it is running you can use the command "mongo" to open up the Mongo DB Shell.


