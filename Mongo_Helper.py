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
def insertTransaction(transactions, date, user, numResults):
	try:
		data = {'access_time': date, 'user_looked_up': user, 'num_tweets': numResults}
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


