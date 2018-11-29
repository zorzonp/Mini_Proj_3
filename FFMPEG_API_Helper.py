####################################################################
##
##  Authors:	  Peter Zorzonello
##  Last Update:  9/15/2018
##  Class:        EC601 - A1
##  File_Name:	  FFMPEG_API_Helper.py
##
##  Description:	
##    This is a library file used to access the FFMPEG API
##
####################################################################

#import required libraries
import os
import ffmpy

####################################################################
##
## Function mergeImages
##
## Description
##   This function takes images stored in a common area and merges
##    them into a video format. The video is stored at the same 
##    location as the images.
## 
## Inputs
##   path: The path to the image directory, where the video lives
##
## Outputs
##   Integer 0 if successful, 1 if failure
##
## Exception Handling
##   Error messages are printed to the console
##   If the video can't be made then it quits the program
##
####################################################################
def mergeImages(path):


	#if the video exists, remove it. If not then it could error out.
	os.system("rm "+path+"out_video.m4v")

	#runs the ffmpeg
	try:
		#os.system("ffmpeg -pattern_type glob -framerate 30 -i '"+path+"*.jpg' "+path+"out_video.m4v")
		ff = ffmpy.FFmpeg(inputs={""+path+"*.jpg": '-framerate 1/5 -pattern_type glob'}, outputs={""+path+"out.m4v": '-y'})
		ff.cmd
		ff.run()
		return 0
	except:
		print("Could not generate video from images. Process needs to exit.")
		return 1


####################################################################
##
## Function reformatImages
##
## Description
##   This function takes images stored in a common area converts them 
##    to all have the same width and a scaled height too keep the aspect 
##    ratio.
## 
## Inputs
##   path: The path to the image directory, where the video lives
##
## Outputs
##   None
##
## Exception Handling
##   Error messages are printed to the console
##
####################################################################
def reformatImages(path):

	#loops over all images and makes them the same size (width and height need to be divisible by 2)
	for file in os.listdir(path):
		if file.endswith(".jpg"):
			ffmpegCmd = ffmpy.FFmpeg(inputs={path+file: None}, outputs={path+file: '-vf scale=690:-2 -y'})
			ffmpegCmd.cmd
			ffmpegCmd.run()
			#os.system("ffmpeg -i "+path+file+" -vf scale=690:-2 "+path+file+" -y")

