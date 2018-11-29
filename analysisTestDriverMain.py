import MySQL_Helper
import Mongo_Helper


try:
	goodToExit = False
	while goodToExit == False:
		dbChoice = input("Please elect the DB to use. Choices are 'Mongo', 'MySQL', or 'exit'.\nAnswer: ")

		if dbChoice == "Mongo":
			goodToExit = True

		elif dbChoice == "MySQL":
			goodToExit = True

		elif dbChoice == "exit":
			exit(1)

	if dbChoice == "MySQL":

		connection = MySQL_Helper.connectToInstance()
		connection = MySQL_Helper.createDB(connection, 'demo')

		goodToExit = False
		while goodToExit == False:
			fnChoice = input("Select the analysis function to test. Choices are: 'label lookup', 'history', 'most used label', 'stats', and 'exit'.\nAnswer: ")

			if fnChoice == "label lookup":
				labelName = input("Enter a label to lookup.\nAnswer: ")
				result = MySQL_Helper.lookUpLabel(connection, labelName)
				print(result)
				print("\n")

			elif fnChoice == "history":
				result = MySQL_Helper.history(connection)
				for r in result:
					print(r)
				print("\n")

			elif fnChoice == "most used label":
				result = MySQL_Helper.mostUsedLabel(connection)
				print("Top Result: ", result["mostPopularLabel"])
				print("2nd: ", result["secondMostPopularLabel"])
				print("3rd: ", result["thirdMostPopularLabel"])
				print("\n")

			elif fnChoice == "stats":
				result = MySQL_Helper.transactionStats(connection)
				print("Average Number of Tweets per transaction: ", result["averageNumTweets"])
				print("Average Number of Images per transaction: ",result["averageNumImages"])
				print("Total number of transaction: ",result["numberOfEntries"])
				print("\n")

			elif fnChoice == "exit":
				exit(1)
	else:

		client = Mongo_Helper.setupClient()
		db = Mongo_Helper.connectToDB(client)
		transactions = Mongo_Helper.connectToTransactions(db)
		labels = Mongo_Helper.connectToLabels(db)

		goodToExit = False
		while goodToExit == False:
			fnChoice = input("Select the analysis function to test. Choices are: 'label lookup', 'history', 'most used label', 'stats', and 'exit'.\nAnswer: ")

			if fnChoice == "label lookup":
				labelName = input("Enter a label to lookup.\nAnswer: ")
				result = Mongo_Helper.lookupLabel(labels, labelName)
				print(result)
				print("\n")

			elif fnChoice == "history":
				result = Mongo_Helper.history(transactions)
				for r in result:
					print(r)
				print("\n")

			elif fnChoice == "most used label":
				result = Mongo_Helper.mostUsedLabel(labels)
				print("Top Result: ", result["mostPopularLabel"])
				print("2nd: ", result["secondMostPopularLabel"])
				print("3rd: ", result["thirdMostPopularLabel"])
				print("\n")

			elif fnChoice == "stats":
				result = Mongo_Helper.transactionStats(transactions)
				print("Average Number of Tweets per transaction: ", result["averageNumTweets"])
				print("Average Number of Images per transaction: ",result["averageNumImages"])
				print("Total number of transaction: ",result["numberOfEntries"])
				print("\n")

			elif fnChoice == "exit":
				exit(1)

except Exception as e:
	print("Error: ", e)

