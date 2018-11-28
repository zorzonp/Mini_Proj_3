####################################################################
##
##  Authors:		Peter Zorzonello
##  Last Update:	11/27/2018
##  Class:			EC601 - A1
##  File_Name:		Main.py
##
##  Description:	
##    This is a control file used to test and call the library 
##      functions created as part of the first Mini-Project
##
####################################################################

#Import the required libraries
import Twitter_API_Helper
import FFMPEG_API_Helper
import Google_API_Helper
import MySQL_Helper
import Mongo_Helper
import time

#global path for JSON credentials
jsonPath = '/Users/peterzorzonello/Downloads/My First Project-a1eeec47076c.json'

####################################################################
##
## Function Main
##
## Description
##   This is the main procedure of this test stub. It calls the 
##    library functions that access the different APIs.
## 
## Inputs
##   None
##
## Outputs
##   None
##
## Exception Handling
##   Error messages are printed to the console
##
####################################################################
def main():
	
	print("\n\nStarting API Project")

	try:
		connection = MySQL_Helper.connectToInstance()
		connection = MySQL_Helper.createDB(connection, 'demo')
		MySQL_Helper.createTableTransactions(connection)
	except Exception as e:
		print("Error: ", e)
		exit()

	try:
		client = Mongo_Helper.setupClient()
		db = Mongo_Helper.connectToDB(client)
		transactions = Mongo_Helper.connectToTransactions(db)
	except Exception as e:
		print("Error: ", e)
		exit()

	#authenticate with Twitter
	twitterClient = Twitter_API_Helper.authenticate()
	
	#find a user
	user = Twitter_API_Helper.findUser(twitterClient)

	#get all their tweets
	tweets = Twitter_API_Helper.getTweets(twitterClient, user)

	
	now = time.strftime('%Y-%m-%d %H:%M:%S')
	Mongo_Helper.insertTransaction(transactions, now, user, len(tweets))

	#filter tweets for images and download the images to path
	result = Twitter_API_Helper.filterTweetsForImages(twitterClient, tweets, user)
	path = result["path"]

	#record the transaction in MySQL
	now = time.strftime('%Y-%m-%d %H:%M:%S')
	MySQL_Helper.insertTransaction(connection, now, user, len(tweets), result["numImages"])
	
	#reform all images in path to be the same size
	#FFMPEG_API_Helper.reformatImages(path)

	#make the images into a video, if falue status will be 1
	
	#status = FFMPEG_API_Helper.mergeImages(path)

	# if status == 1:
		# print ("FFMPEG could not make video. Annotateing images instead.")
		#authenticate with Google
	Google_API_Helper.authenticate(jsonPath)
	try:
		Google_API_Helper.annotateImages(path)
	except:
		print("Could not annotate images. Google may not have been able to authenticate your credentials")
	
	#authenticate with Google
	# Google_API_Helper.authenticate(jsonPath)

	# try:
	# 	#annotate video
	# 	video = Google_API_Helper.openVideo(path)
	# 	results = Google_API_Helper.annotate(video)

	# 	#print results
	# 	Google_API_Helper.printResults(path, results)
	# except:
		print("Could not annotate video. Google may not have been able to authenticate your credentials")
	
	print("\nEnding API Project\n\n")




#Call the main function
main()
