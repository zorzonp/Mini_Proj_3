####################################################################
##
##  Authors:		Peter Zorzonello
##  Last Update:	9/15/2018
##  Class:			EC601 - A1
##  File_Name:		Twitter_API_Helper.py
##
##  Description:	
##    This is a library file containing functions that utilize the 
##      Tweepy API.
##
####################################################################

#import required libraries
import tweepy
import twitter_globals_secret
import os
import wget

####################################################################
##
## Function Authenticate
##
## Description
##   This procedure uses the consumer key and secret, as well as 
##    the access token and secret to authenticate with Twitter.
##    Authentication uses OAuth
## 
## Inputs
##   None
##
## Outputs
##   An instance of the Tweepy API. 
##
## Exception Handling
##   Error messages are printed to the console
##   If the process could not authenticate with Twitter the process 
##     is terminated.
##
####################################################################
def authenticate():
	#this is the consumer key and secret, needed to authenticate with Twitter
	CONSUMER_KEY = twitter_globals_secret.CONSUMER_KEY
	CONSUMER_SECRET = twitter_globals_secret.CONSUMER_SECRET
	ACCESS_TOKEN = twitter_globals_secret.ACCESS_TOKEN
	ACCESS_TOKEN_SECRET = twitter_globals_secret.ACCESS_TOKEN_SECRET

	print ("\n\nChecking on Twitter.com.......")

	#check on twitter.com by pinging it. If it responds we know 1) we have an internet connection and 2) Twitter.com is up
	if os.system("ping -c 1 twitter.com >nul 2>&1"):
		#if Twitter could not be reached then alert the user
		print("\n")
		print("Could not reach Twitter.")
		print("Please check your internet connection and try again.")
		print("If the problem persists then Twitter could be down.\n\n")
		exit(1)

	else:
		print("Twitter is live!")

		try:
			auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
			auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

			clientApi = tweepy.API(auth)

			#try and use the API to see if it errors
			clientApi.verify_credentials()
			return clientApi
		
		except tweepy.TweepError as e:
			print ("Unable to authenticate with Twitter.\n Program is terminating.\n\n")
			print ("Error: ", e)
			exit(1)



####################################################################
##
## Function FindUser
##
## Description
##   This attempts to find a Twitter profile. It prompts the user
##    to enter a Twitter handle, if the handle is valid, and 
##    if it can find the user it returns the Twitter handle.
##    If it cannot find the user or the handle is not in the correct 
##    format it will keep prompting the user until they exit. 
## 
## Inputs
##   api: An instance of the tweepy API, needed to call the API functions
##
## Outputs
##   A Twitter handle
##
## Exception Handling
##   Error messages are printed to the console
##   If the user cannot provide a valid Twitter handle the process
##    terminates.
##
####################################################################
def findUser(api):

	while 1 == 1:
		#ask the user for a Twitter username
		userName = input("Please enter a Twitter handle (enter 'exit' to quit): ")

		#check the handle for proper syntax
		index = userName.find('@')

		
		#if this is exit then end program
		if userName == 'exit':
			print('Bye!')
			exit(1)

		#if the first character is not @ then this is a handle 	
		elif index != 0:
			print("Not a valid Twitter handle.")

		#if this is a handle
		else:
			try:
				user = api.get_user(userName)
				print("\n")
				print("Found user: " + user.name)
				break

			except:
				print("Not a valid Twitter handle.")
					

	return userName

###################################################################
##
## Function getTweets
##
## Description
##   This procedure returns all the tweets from a user's timeline
## 
## Inputs
##   api: An instance of the tweepy API, needed to call the API functions
##   userName: A Twitter handle. The user's who's tweets to get.
##
## Outputs
##   An array of Tweet objects
##
## Exception Handling
##   Error messages are printed to the console
##
####################################################################
def getTweets(api, userName):

	#get all the user tweets
	tweets = []
	num_tweets_asked = 0
	tweets_num = 0

	#Ask the user how many tweets they want
	while True:
		num_tweets_asked = input("How many tweets whould you like to retrieve?\nEnter a number, all for all tweets, or exit to quit.\nKeep in mind number of tweets is not number of images.\n")
		if num_tweets_asked != 'exit':
			if num_tweets_asked == 'all':
				
				answer = input("Getting all tweets could take a long time. Are you sure? [y,n]")
				while answer != 'y' or answer != 'n':
					
					if answer == 'y':
						break
					elif answer == 'n':
						break
					else:
						answer = input("Getting all tweets could take a long time. Are you sure? [y,n]")


				if answer == 'y':
					break

			else:
				try:
					tweets_num = int(num_tweets_asked)
					break
				except:
					print("Not a valid input.")

		else:
			exit()

    #get the tweets for the user
	print("Fetching Tweets...")

	#get all tweets
	if num_tweets_asked == 'all':
		for page in tweepy.Cursor(api.user_timeline, screen_name=userName).pages():
			tweets = tweets + page

	#get tweets until we get the number requested 
	else:
		for page in tweepy.Cursor(api.user_timeline, screen_name=userName).pages():
			tweets = tweets + page
			if len(tweets) >= tweets_num:
				break

	print("Found: " + str(len(tweets)) + " Tweets")
	return tweets



###################################################################
##
## Function filterTweetsForImages
##
## Description
##   This procedure examines all the tweets provided and downloads
##     any images from the tweets.
## 
## Inputs
##   api: An instance of the tweepy API, needed to call the API functions
##   tweets: An array of tweet objects
##   userName: the twitter handle of the user
##
## Outputs
##   path: the path to the images folder
##
## Exception Handling
##   Error messages are printed to the console
##
####################################################################
def filterTweetsForImages(api, tweets, userName):

	#make a directory for the images(unless one exists)
	if not os.path.isdir("./img"):
		os.system("mkdir img")

	#make a new directory for the user 
	if os.path.isdir("./img/"+userName):
		os.system("rm -rf ./img/"+userName)
	os.system("mkdir img/"+userName)
	path = "./img/"+userName

	counter=0
	#loop over all tweets for the media tweets
	print("Downloading Images...")
	for tweet in tweets:

		#only look at media tweets
		if "media" in tweet.entities:
			
			url = tweet.entities["media"][0]["media_url"]
			fileName = path+"/IMG_"+str(counter)+".jpg"
			
			#attempt to download the photo from Twitter
			try:
				wget.download(url=url, out=fileName)
				counter = counter + 1
			except:
				print("\nFound an invalid URL. Skipping.")

	print("\nDownloaded " + str(counter) + " tweets with images.")

	path = path + "/"
	return path