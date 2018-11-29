import pymongo
from pymongo import MongoClient

#Sets up a MongoDB client with a running instance of MongoDB. MongoDB must be running on localhost. 
def setupClient():
	try:
		client = MongoClient()
		client = MongoClient('localhost', 27017)

		return client
	except Exception as e:
		print ("Unable to connect to the MongoDB Instance.\n Program is terminating.\n\n")
		exit()

#Connects to the demo database in the running instance of MongoDB. The client is passed in.
def connectToDB(client):
	try:
		db = client.demo
		return db
	except Exception as e:
		print ("connectToDB Error: ", e)
		exit()

#tries and create or connect to the transactions collection. The MongoDB database object is passed in.
def connectToTransactions(db):
	
	try:
		transactions = db['transactions']
		return transactions

	except Exception as e:
		print ("connectToTransactions Error: ", e)
		exit()
	
#Inserts a transaction into the MongoDB transactions collection. This is run every time a user makes a request for Twitter images
#the transactions collection is passed in as a MongoDB collections object, 
#the date and the user are passed in as strings. The number of results is an integer.
def insertTransaction(transactions, date, user, numResults, numImages):
	try:
		data = {'access_time': date, 'user_looked_up': user, 'num_tweets': numResults, 'num_images':numImages}
		results = transactions.insert_one(data)
	except Exception as e:
		print ("insertTransaction Error: ", e)
		exit()

#Dropts any collection from the database. Must pass in the collection name as a string. The DB should be an MongoDB database object
def dropCollection(db, collectionName):
	try:
		collection = db[collectionName]
		collection.drop()
	except Exception as e:
		print ("dropCollection Error: ", e)
		exit()

#Tries and creates or connects to the labels collection in the MongoDB. The MongoDB database object is passed in
def connectToLabels(db):
	try:
		labels = db['labels']
		return labels
	except Exception as e:
		print ("Warning!! Could not create or connect to labels collection. No Label data will be stored from this transaction.")
		print ("Error: ", e)

#Checks if the label already exists. Must pass in the labels collection as a collection object and the label name as a string.
#returns ture if it exists in the collection, false if not. 
def checkLabelExists(labels, labelName):
	try:
		results = labels.find({'label':labelName})
		if (results.count() > 0):
			return True
		else:
			return False

	except Exception as e:
		print ("checkLabelExists Error: ", e)

#Inserts the info for a label. Lables must be the collection object, labelName is a string and numOccurrences is an integer
def insertLabel(labels, labelName, numOccurrences):
	try:
		data = {'label': labelName, 'numberOccurrences': numOccurrences}
		results = labels.insert_one(data)
	except Exception as e:
		print ("insertLabel Error: ", e)

#if the label already exists then update the number of occurances. labels is the collection object and labelName is a string
def updateNumOccurrences(labels, labelName):
	try:
		results = labels.find({'label':labelName})
		if (results.count() > 0):
			firstResult = results[0]
			numOccurrences = firstResult['numberOccurrences']
			numOccurrences = numOccurrences + 1

			results = labels.update({'label':labelName}, {'$set':{'numberOccurrences':numOccurrences}})
	except Exception as e:
		print ("updateNumOccurrences Error: ", e)

#associates a username with a label. LableName and userName are strings. Labels is a collection object. 
def addUserToLabel(labels, labelName, userName):
	try:
		results = labels.find({'label':labelName})
		if (results.count() > 0):
			firstResult = results[0]
			numFields = len(firstResult)
			#3 fields would indicate id, label, and numOccurance
			if numFields < 4:
				users = [userName]
				results = labels.update({'label':labelName}, {'$set':{'users':users}})
			
			else:#4 fields indicate the presence of a users field
				
				#check the presence of all the users to make sure not duplicate
				users = firstResult['users']

				#if the user is not already associated with this label then add them to the list of associated users
				if not userName in users:
					users.append(userName)
					results = labels.update({'label':labelName}, {'$set':{'users':users}})
					
	except Exception as e:
		print ("addUserToLabel Error: ", e)

########################################################################################################################
## The following functions are for analysis


def lookupLabel(labels, labelName):
	try:
		results = labels.find({"label":labelName})
		
		if results != None:
			returnResult = {"label":results[0]["label"],"numberOccurrences":results[0]["numberOccurrences"],"users":results[0]["users"]}
			return returnResult
		else:
			print("Label "+labelName+" not found.")
	except Exception as e:
		print("Unable to look up label " + labelName)
		print ("Mongo_Helper.lookupLabel error: ", e)

def mostUsedLabel(labels):
	try:
		topHit = {"label":"","numberOccurrences": 0,"users":""}
		secondHit = {"label":"","numberOccurrences":0,"users":""}
		thirdHit = {"label":"","numberOccurrences":0,"users":""}

		results = labels.find()

		#only try and find the top results if something was returned
		if results != None:
			#loop over all the results
			for result in results:
				#replace the top result if the new result is more
				if result["numberOccurrences"] > topHit["numberOccurrences"]:
					thirdHit = secondHit
					secondHit = topHit
					topHit = result
				#replace the second top result if the new result is more
				elif result["numberOccurrences"] > secondHit["numberOccurrences"]:
					thirdHit = secondHit
					secondHit = result
								
				#replace the third top result if the new result is more
				elif result["numberOccurrences"] > thirdHit["numberOccurrences"]:
					thirdHit = result
			returnResult = {"mostPopularLabel":topHit, "secondMostPopularLabel":secondHit, "thirdMostPopularLabel":thirdHit}
			return returnResult
		else:
			print("There are no labels in the table.")

	except Exception as e:
		print ("Mongo_Helper.mostUsedLabel error: ", e)


#return statistics about all the transactions 
def transactionStats(transactions):
	try:
		results = transactions.find()
		
		sumTweets = 0
		numResults = 0
		sumImages = 0

		for result in results:
			sumTweets = sumTweets + result["num_tweets"]
			sumImages = sumImages + result["num_images"]
			numResults = numResults + 1

		averageNumTweets = sumTweets/numResults
		averageNumImages = sumImages/numResults

		returnResult = {"averageNumTweets":averageNumTweets, "averageNumImages":averageNumImages, "numberOfEntries":numResults}

		return returnResult

	except Exception as e:
		print ("Mongo_Helper.transactionStats Error: ", e)

#returns a history of all the transactions in the transactions collection
def history(transactions):
	try:
		results = transactions.find()
		
		returnResult =[]
		#we must reformat the results so that all the fields are in the same order. 
		#Mongo can sometimes store the same set of fields in different orders
		for result in results:
			tmp = {"date":result["access_time"],"user":result["user_looked_up"], "numTweets":result["num_tweets"], "numImages":result["num_images"]}
			returnResult.append(tmp)

		return returnResult
			
	except Exception as e:
		print ("Mongo_Helper.history error: ", e)





