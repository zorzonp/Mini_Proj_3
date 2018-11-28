import MySQLdb
import sqlConnectInfo



HOST = "localhost" 

#This function connects to a MySQL instance and returns the connection
def connectToInstance():
	USER = sqlConnectInfo.USERNAME
	PASSWORD = sqlConnectInfo.PASSWORD
	
	#attempt to connect to the instance of the MySQL
	try:
		connection = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWORD)
		return connection

	#If the connection could not be made, this couble be becasue of bad username/password or no instance found at HOST
	#for security do not let the user know the reason. 
	except:
		print ("Unable to connect to the MySQL Instance.\n Program is terminating.\n\n")
		exit(1)

#this function will try and create a database on the instance
#Returns a connection to the db, even if the db exists.
def createDB(connection, dbName):
	USER = sqlConnectInfo.USERNAME
	PASSWORD = sqlConnectInfo.PASSWORD

	try:
		#Try and make a db using dbName
		cur = connection.cursor()
		cur.execute('CREATE DATABASE '+ dbName +';')

		#connect to the new db and return the connection
		connection = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWORD, db=dbName)
		return connection

	except MySQLdb.Error as e:
		
		#if the error is that the db already exists, then just connect to it and return the connection
		if(e.args[0] == 1007):
			print("Database "+ dbName +" already exists.")
			connection = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWORD, db=dbName)
			return connection

		#unknow error, let the user know and exit
		else:
			print ("Unable to create database" + dbName +".\n Program is terminating.\n\n")
			print("Error: ", e)
			exit(1)

	#unknow error, let the user know and exit
	except Exception as e:
		print ("Unable to create database" + dbName +".\n Program is terminating.\n\n")
		print("Error: ", e)
		exit(1)

#Tries and creates the table to log user transactions
def createTableTransactions(connection):
	try:
		cur = connection.cursor()
		cur.execute('CREATE TABLE IF NOT EXISTS transactions (id int(11) NOT NULL AUTO_INCREMENT, access_time datetime NOT NULL, user_looked_up varchar(50) NOT NULL, num_tweets int(11) NOT NULL, num_images int(11), PRIMARY KEY (id));')
		
	except MySQLdb.Error as e:
		if(e.args[0] == 1050):
			print ("Table transactions already exists.")
		else:
			print("Error: ", e)
		exit(1)

	except Exception as e:

		print("Error: ", e)
		exit(1)

#Inserts a transaction into the transactions table
def insertTransaction(connection, date, user, num_results, num_images):
	try:
		cur = connection.cursor()
		cur.execute('INSERT INTO transactions (access_time, user_looked_up, num_tweets, num_images) VALUES(%s, %s, %s, %s);', (date, user, num_results, num_images))
		connection.commit()
	except Exception as e:
		connection.rollback()
		print("Error: ", e)
		print("WARNING!! Entry not added to the transactions table!")

#drops the labels tabel, useful for debugging
def dropTableLabel(connection):
	try:
		cur = connection.cursor()
		cur.execute('DROP TABLE labels')
	except Exception as e:
		print ("dropTableLabel Error: ", e)
		exit(1)

#this tries and creates a table that will hold all descriptions and the number of occurances
def createTableLabel(connection):
	try:
		cur = connection.cursor()
		cur.execute('CREATE TABLE IF NOT EXISTS labels (label varchar(50) NOT NULL, num_occurrences int(50) NOT NULL, usernames longtext, PRIMARY KEY (label));')
	except MySQLdb.Error as e:
		if(e.args[0] == 1050):
			print ("Table transactions already exists.")
		else:
			print("Error: ", e)
		exit(1)

	except Exception as e:
		print ("Error: ", e)
		exit(1)

#Inserts an entry into the labels table
def insertTableLabel(connection, labelName, numOccurrences):
	try:
		cur = connection.cursor()
		cur.execute('INSERT INTO labels (label, num_occurrences) VALUES(%s, %s);', (labelName, numOccurrences))
		connection.commit()
	except Exception as e:
		connection.rollback()
		print("Error: ", e)
		print("WARNING!! Entry not added to the labels table!")

#Associates a user with a label
def addUserToLabel(connection, user, labelName):
	try:
		cur = connection.cursor()
		cur.execute('SELECT * FROM labels WHERE label = %s', [labelName])
		#just need the first one, as only one should be in the table as lables are primary keys
		myresult = cur.fetchone()

		#get the textblob of usernames
		usernamesBlob = myresult[2]

		#if there is no users for this label then don't try and split the text
		if not usernamesBlob == None: 

			#parse this into a python list
			usernameList = usernamesBlob.split(',')
			
			#if the user associated with this label don't add them to this list
			if user in usernameList:
				pass
			
			else:
				#add the user to the text list, comma seprated list.
				usernamesBlob = usernamesBlob + user + ","

				#update the DB
				cur.execute('UPDATE labels SET usernames = %s WHERE label = %s', (usernamesBlob,labelName))
				connection.commit()
		else:
			#add the user to the table if this is the first user
			usernamesBlob = user + ","
			cur.execute('UPDATE labels SET usernames = %s WHERE label = %s', (usernamesBlob,labelName))
			connection.commit()

	except Exception as e:
		connection.rollback()
		print("Error: ", e)
		print("WARNING!! Entry not updated in the labels table!")

#Adds one to the number of occurrences for a spicific label
def updateNumOccurrences(connection, labelName):
	try:
		cur = connection.cursor()
		cur.execute('UPDATE labels SET num_occurrences = num_occurrences + 1 WHERE label = %s', [labelName])
		connection.commit()
	except Exception as e:
		connection.rollback()
		print("Error: ", e)
		print("WARNING!! Entry not updated in the labels table!")

#checks if a label exists in the labels table. If the label is there return a True, else return False
def checkLabelExists(connection, labelName):
	try:
		cur = connection.cursor()
		cur.execute("SELECT COUNT(1) FROM labels WHERE label = %s", [labelName])
		myresult = cur.fetchone()
		if myresult[0] == 1:
			return True
		else:
			return False
		
	except Exception as e:
		print("checkLabelExists Error: ", e)



########################################################################################################################
## The following functions are for analysis

#looks up a spicific label and return its statistics 
def lookUpLabel(connection, labelName):
	try:
		cur = connection.cursor()
		cur.execute("SELECT * FROM labels WHERE label = %s", [labelName])
		myresult = cur.fetchone()
		if myresult != None:
			returnResult = {"label":myresult[0],"numberOccurrences":myresult[1],"users":myresult[2]}
			return returnResult
		else:
			print("Label "+labelName+" not found.")
	except Exception as e:
		print("Unable to look up label " + labelName)
		print("lookUpLabel error: ", e)

#finds the most used labels and return them
def mostUsedLabel(connection):
	try:

		topHit = ["",0,""]
		secondHit = ["",0,""]
		thirdHit = ["",0,""]

		cur = connection.cursor()
		cur.execute("SELECT * FROM labels")
		myresults = cur.fetchall()
		#only try and find the top results if something was returned
		if myresults != None:
			#loop over all the results
			for result in myresults:
				#replace the top result if the new result is more
				if result[1] > topHit[1]:
					thirdHit = secondHit
					secondHit = topHit
					topHit = result
				#replace the second top result if the new result is more
				elif result[1] > secondHit[1]:
					thirdHit = secondHit
					secondHit = result
								
				#replace the third top result if the new result is more
				elif result[1] > thirdHit[1]:
					thirdHit = result
			returnResult = {"mostPopularLabel":topHit, "secondMostPopularLabel":secondHit, "thirdMostPopularLabel":thirdHit}
			return returnResult
		else:
			print("There are no labels in the table.")
	except Exception as e:
		print("mostUsedLabel error: ", e)

#return statistics about all the transactions 
def transactionStats(connection):
	try:
		cur = connection.cursor()
		cur.execute("SELECT * FROM transactions")
		myresults = cur.fetchall()

		sumTweets = 0
		numResults = 0

		sumImages = 0

		for result in myresults:
			sumTweets = sumTweets + result[3]
			sumImages = sumImages + result[4]
			numResults = numResults + 1

		averageNumTweets = sumTweets/numResults
		averageNumImages = sumImages/numResults

		returnResult = {"averageNumTweets":averageNumTweets, "averageNumImages":averageNumImages, "numberOfEntries":numResults}

		return returnResult
	except Exception as e:
		print("transactionStats error: ", e)

#returns the entire history from transactions table
def history(connection):
	try:
		cur = connection.cursor()
		cur.execute("SELECT * FROM transactions")
		myresults = cur.fetchall()
		returnResult =[]

		for result in myresults:
			tmp = {"id":result[0] , "date":result[1], "user":result[2] ,"numTweets":result[3],"numImages":result[4] }
			returnResult.append(tmp)

		return returnResult
	except Exception as e:
		print("history error: ", e)	