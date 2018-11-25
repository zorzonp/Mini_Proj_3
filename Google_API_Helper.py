####################################################################
##
##	Authors:		Peter Zorzonello
##	Last Update:	9/16/2018
##	Class:			EC601 - A1
##	File_Name:		Google_API_Helper.py
##
##	Description:	
##		This is a library file containing functions that utilize 
##			the Google Vision API
##
####################################################################

#import libraries
import io
import os
from google.cloud import vision
from google.cloud.vision import types
from google.cloud import videointelligence
import MySQL_Helper

####################################################################
##
## Function Authenticate
##
## Description
##   This procedure authenticates with the Google services using a 
##    locally stored JSON file.
## 
## Inputs
##   jsonPath: path to JSON credentials for Google APIs
##
## Outputs
##   None 
##
## Exception Handling
##   Error messages are printed to the console
##   If the process could not authenticate with Google the process 
##     is terminated.
##
####################################################################
def authenticate(jsonPath):
	
	print ("\n\nChecking on Google.com.......")
	
	#test that Google is live
	if os.system("ping -c 1 google.com >nul 2>&1"):
		#if Twitter could not be reached then alert the user
		print("\n")
		print("Could not reach Google.")
		print("Please check your internet connection and try again.")
		print("If the problem persists then Google could be down.\n\n")
		exit(1)

	else:
		print("Google.com is live.")
		#sets the environmet variable needed for the Google credientials
		os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = jsonPath
	

####################################################################
##
## Function openVideo
##
## Description
##   This procedure opens a video file stored locally
## 
## Inputs
##   path: path to the video to use
##
## Outputs
##   An opened video file 
##
## Exception Handling
##   Error messages are printed to the console
##   If the file cannot be found or the file cannot be opened then 
##     return 1
##
####################################################################
def openVideo(path):
	try:
		path = path+'out.m4v'
		with io.open(path, 'rb') as movie:
			video = movie.read()
			return video
	except:
		print("Video could not be opened.")
		return 1

####################################################################
##
## Function annotate
##
## Description
##   This sends a video to Google to be annotated by their API
## 
## Inputs
##   video: The video to annotate
##
## Outputs
##   The annotated results returned by the API
##
## Exception Handling
##   Error messages are printed to the console
##   If the annotation was unsuccessful returns 1
##
####################################################################
def annotate(video):
	if video != 1:
		try:
			#set up the API client
			googleVideoClient = videointelligence.VideoIntelligenceServiceClient()

			#the features to look for are labels
			features = [videointelligence.enums.Feature.LABEL_DETECTION]

			print("Annotating video ......")
			#Annotate the Video
			annotation = googleVideoClient.annotate_video(features=features, input_content=video)

			print ("Processing the video for labels ........")

			try:
				result = annotation.result(90)
				if len(result.annotation_results) >= 1:
					print('\nFinished processing results.')
					return result
				
				#no results
				else:
					print("Google Video Intelligence could not find any results.")
					return 1
			
			#error getting results
			except Exception as e:
				print("The results could not be generated.")
				print(str(e))
				return 1

		#error in annotating
		except Exception as e:
			print("Could not annotate the video.")
			print(str(e))
			return 1

	#the video was never opend
	else:
		return 1



####################################################################
##
## Function annotateImages
##
## Description
##   This procedure loops over the images in the directory and 
##    passes them to Google Vision API for analysis.
## 
## Inputs
##   path: the path the video. Same directory where the results will be
##
## Outputs
##   None
##
## Exception Handling
##   Error messages are printed to the console
##
####################################################################
def annotateImages(path):

	print("Doing annotations on images in "+ path + ".........")
	googleImageClient = vision.ImageAnnotatorClient()

	#get the user from the path, needed for some of the SQL stuff
	pathElements = path.split('/')
	user = pathElements[len(pathElements)-2]


	#set up the required SQL stuff to add and query
	try:
		connection = MySQL_Helper.connectToInstance()
		connection = MySQL_Helper.createDB(connection, 'demo')
		MySQL_Helper.createTableLabel(connection)
	except Exception as e:
		print("Error in annotateImages: ", e)

	#sets up an output file
	imageDescFile = open(path+"image_descriptions.txt", "w")

	#loop over all files in directory
	for file in os.listdir(path):

		#only on files ending with "jpg"
		if file.endswith(".jpg"): 

			imageDescFile.write(os.path.join(path, file) + "\n")

			# The name of the image file to annotate
			fileName = os.path.join(os.path.dirname(__file__), path+file)

			# Loads the image
			with io.open(fileName, 'rb') as image_file:
				content = image_file.read()

			image = types.Image(content=content)

			#Gets the labels from Google
			response = googleImageClient.label_detection(image=image)
			labels = response.label_annotations

			imageDescFile.write('\tLabels\n')
			for label in labels:
				imageDescFile.write("\t\t"+label.description+": ")
				confidence = label.score * 100.0
				imageDescFile.write(str(round(confidence,2))+"%\n")

				#Check if the label exists
				exists = MySQL_Helper.checkLabelExists(connection, label.description)

				#if it exists add to its occurance counter
				if exists:
					MySQL_Helper.updateNumOccurrences(connection, label.description)
					#associate the user with this label
					MySQL_Helper.addUserToLabel(connection, user, label.description)

				#if it does not exist then create the first occurance
				else:
					MySQL_Helper.insertTableLabel(connection, label.description, 1)

					#associate the user with this label
					MySQL_Helper.addUserToLabel(connection, user, label.description)

			imageDescFile.write("\n")
	print("File: image_descriptions.txt has been written to " + path)

####################################################################
##
## Function printResults
##
## Description
##   This procedure loops over the results of an annotated video
##     and prints them to the console for the user
## 
## Inputs
##   path: the path the video. Same directory where the results will be
##   results: the annotated results
##
## Outputs
##   None
##
## Exception Handling
##   Error messages are printed to the console
##
####################################################################
def printResults(path, results):

	status = 0
	#check if the results are just an integer
	if results != 1:
		#get the different types of labels 
		segment_labels = results.annotation_results[0].segment_label_annotations
		shot_labels = results.annotation_results[0].shot_label_annotations

		#if the results have no labels then the API did not work
		if len(segment_labels) < 1 and len(shot_labels) < 1:
			print("The results for this video were empty.")
			print("Google Video Intelligance could not assign labels to this video.")
			print("Annotating images instead.")
			annotateImages(path)

		#print the results
		else:
			videoDescFile = open(path + "video_descriptions.txt", "w")

			#print the segment labels if there are any
			if len(segment_labels) > 0:
				videoDescFile.write("Printing Segment Results for " + str(len(segment_labels)) + " segments\n")
				
				#print the segment data
				for i, segment_label in enumerate(segment_labels):
					
					videoDescFile.write('Label: '+ str(segment_label.entity.description) + "\n")
					
					#some lables may be part of a category
					for category_entity in segment_label.category_entities:
						videoDescFile.write("\tCategory: "+ str(category_entity.description) + "\n")

					for i, segment in enumerate(segment_label.segments):
						confidence = (segment.confidence) * (100.0)
						videoDescFile.write("\tConfidence: "+ str(round(confidence,2)) + "%\n")
					videoDescFile.write('\n')

			#print the shot labels if no segment labels
			elif len(shot_labels) > 0:
				videoDescFile.write("Printing Shot Results for " + str(len(shot_labels)) + " shots\n")

				#print the shot data
				for i, shotLabel in enumerate(shot_labels):
					videoDescFile.write('Label: '+ str(shotLabel.entity.description) + "\n")

					#check if the shot has a category
					for categoryEntity in shotLabel.category_entities:
						videoDescFile.write("\tCategory: " + str(categoryEntity.description) + "\n")

					for i, shot in enumerate(shotLabel):
						confidence = (shot.confidence) * (100.0)
						videoDescFile.write("\tConfidence: "+ str(round(confidence,2)) + "%\n")
					videoDescFile.write('\n')

	else:
		print("There were no results. Annotating images instead.")
		annotateImages(path)

