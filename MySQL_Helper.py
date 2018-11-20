import MySQLdb
import sqlConnectInfo



HOST = "localhost" 

#This function connects to a MySQL instance and returns the connection
def connectToInstance():
	USER = sqlConnectInfo.USERNAME
	PASSWORD = sqlConnectInfo.PASSWORD
	try:
		connection = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWORD)
		return connection
	except:
		print ("Unable to connect to the MySQL Instance.\n Program is terminating.\n\n")
		exit(1)

#this function will try and create a database on the instance
#Returns a connection to the db, even if the db exists.
def createDB(connection, dbName):
	USER = sqlConnectInfo.USERNAME
	PASSWORD = sqlConnectInfo.PASSWORD

	try:
		cur = connection.cursor()
		cur.execute('CREATE DATABASE '+ dbName +';')
		connection = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWORD, db=dbName)
		return connection

	except MySQLdb.Error as e:
		if(e.args[0] == 1007):
			print("Database "+ dbName +" already exists.")
			connection = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWORD, db=dbName)
			return connection

	except Exception as e:
		print ("Unable to create database" + dbName +".\n Program is terminating.\n\n")
		print("Error: ", e)
		exit(1)

def createTableTransactions(connection):
	try:
		cur = connection.cursor()
		cur.execute('CREATE TABLE IF NOT EXISTS transactions (id int(11) NOT NULL AUTO_INCREMENT, access_time datetime NOT NULL, user_looked_up varchar(50) NOT NULL, num_results int(11) NOT NULL, PRIMARY KEY (id));')

	except Exception as e:
		print("Error: ", e)
		exit(1)