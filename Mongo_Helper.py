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

