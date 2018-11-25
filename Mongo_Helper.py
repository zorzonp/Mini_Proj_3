import pymongo
from pymongo import MongoClient

def setupClient():
	client = MongoClient()
	client = MongoClient('localhost', 27017)
	print(client.database_names())

	return client

def connectToDB(client):
	db = client.demo
	print(db.collection_names())
	return db

def connectToTransactions(db):
	
	transactions = db['transactions']
	print(db.collection_names())

	return transactions

def insertTransaction(transactions, date, user, numResults):

	data = {'access_time': date, 'user_looked_up': user, 'num_tweets': numResults}
	results = transactions.insert_one(data)
	print(results)

def dropCollection(db, collectionName):
	collection = db[collectionName]
	collection.drop()