# Add in os support to check for files
import os

# Add in the pandas module for excel support
import pandas as pd

# Add in sqlite3 support
import sqlite3
from sqlite3 import Error

# Database Connection Varaible
conn = None

# Checks to see if there is already a database file created
def doesDatabaseExist():
	return os.path.exists("Redemption_TCG.db")

# Check to see if a specific database table exists
def doesTableExists(tableName):
	pass

def createDatabaseTable(tableName, createTableCommand):
	global conn
	try:
		print(f"trying to create table: {tableName} - {createTableCommand}")
		curr = conn.cursor()
		curr.execute(createTableCommand)
		result = curr.execute("SELECT name from sqlite_master")
		print(result.fetchone())
	except Error as e:
		print(e)

# If there is no database found, then create one with all the correct tables
def createDatabaseConnection():
	# Let function know to ise global conn variable instead of created a new local one
	global conn
	
	# Variable to return whether database connectiom was created
	isDBConnectionCreated = False
	
	# Try to create the database connection, if the file doesn't exist it will be created
	try:
		conn = sqlite3.connect("Redemption_TCG.db")
		isDBConnectionCreated = True
		#print(sqlite3.version)
	except Error as e:
		print(e)
	
	return isDBConnectionCreated

def isDatabaseConnected():
	# Check to see if the connection variable has data written to it, if it does then return true, else return false
	if conn:
		return True
	else:
		return False

def closeDatabaseConnection():
	# Variable to return whether database connection was closed
	isDBConnectionClosed = False
	
	# Try to close the database connection if it exists
	try:
		if conn:
			conn.close()
			isDBConnectionClosed = True
	except Error as e:
		print(e)
	
	return isDBConnectionClosed

def generateRedemptionDB():

	print("Reading Redemption Card List XLSX File...")
	
	# Read the specified excel file and store it
	excelFile = pd.ExcelFile('Redemption Card List.xlsx')
	
	curr = conn.cursor()
	
	print("Gathering Card Sets Information...")
	
	# Read the Sets worksheet to get the name of every set
	setSheet = pd.read_excel(excelFile, 'Sets')
	
	setSheet = setSheet.reset_index()
	
	redemptionSets = []
	
	for index, row in setSheet.iterrows():
		redemptionSets.append([row[1], row[2].split('(')[0].strip(), row[2].split('(')[1].split(')')[0], row[3]])
	
	print("Card Sets information retrieved, populating Redemption TCG Database...")
	
	curr = conn.cursor()
	
	for redemptionSet in redemptionSets:
		#print(f"Current Set: {redemptionSet[1]}")
		curr.execute("INSERT INTO Card_Sets (ABBREVIATION, NAME, YEAR, SYMBOL) VALUES (?, ?, ?, ?)", redemptionSet)
	
	results = curr.execute("SELECT * FROM Card_Sets").fetchall()
	
	for result in results:
		print(f"ID: {result[0]}, ABBREVIATION: {result[1]}, NAME: {result[2]}, YEAR: {result[3]}, SYMBOL: {result[4]}")
	
	print("Gathering All Cards...")
	
	# Read the specifice worksheet in the excel file and store it
	cardSheet = pd.read_excel(excelFile, 'Sets Card List')
	
	# Reset the index for the worksheet so it will start at 0
	cardSheet = cardSheet.reset_index()
	
	redemptionCards = []
	
	# Loop to iterate through all the rows
	for index, row in cardSheet.iterrows():
		redemptionCards.append([row['Name'], row['#'], row['Set'], row['Type'], row['Brigade'], row['Strength'], row['Toughness'], row['Class'], row['Identifier'], row['Special Ability'], row['Rarity'], row['Book'], row['Chapter'], row['Verse'], row['Alignment'], row['Legality'], row['Artist']])
		
	print("Inserting Cards Into Database...")
	
	for redemptionCard in redemptionCards:
		curr.execute("INSERT INTO Cards (NAME, NUMBER, SET_ID, TYPE, BRIGADE, STRENGTH, TOUGHNESS, CLASS, IDENTIFIER, SPECIAL_ABILITY, RARITY, BOOK, CHAPTER, VERSE, ALIGNMENT, LEGALITY, ARTIST, NEEDED, TOTAL, FILE) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0, 0)", redemptionCard)
	
	conn.commit()
	
	print(redemptionCards)

def main():
	databaseTables = [["Card Sets", """CREATE TABLE IF NOT EXISTS Card_Sets (ID INTEGER PRIMARY KEY AUTOINCREMENT, ABBREVIATION VARCHAR(10) NOT NULL, NAME TEXT NOT NULL, YEAR INT NOT NULL, SYMBOL TEXT NOT NULL);"""], ["Cards", """CREATE TABLE IF NOT EXISTS Cards (ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT NOT NULL, NUMBER INTEGER, SET_ID TEXT NOT NULL, TYPE TEXT NOT NULL, BRIGADE TEXT NOT NULL, STRENGTH INTEGER NOT NULL, TOUGHNESS INTEGER NOT NULL, CLASS TEXT NOT NULL, IDENTIFIER TEXT NOT NULL, SPECIAL_ABILITY TEXT NOT NULL, RARITY TEXT NOT NULL, BOOK TEXT NOT NULL, CHAPTER TEXT NOT NULL, VERSE TEXT NOT NULL, ALIGNMENT TEXT NOT NULL, LEGALITY TEXT NOT NULL, ARTIST TEXT NOT NULL, NEEDED INTEGER NOT NULL, TOTAL INTEGER NOT NULL, FILE TEXT NOT NULL);"""]]
	
	print("Checking to see if redemption.db datbase exists...")

	# Check to see if database doesn't exist	
	if doesDatabaseExist() == False:
		# Redemption.db database was not found
		print("Database not found, creating database.")
		
		# Try to create the redemption.db database
		if createDatabaseConnection():
			print("Database was created successfully.")
			print("Attempting to create database tables...")
			
			for i in range(len(databaseTables)):
				createDatabaseTable(databaseTables[i][0], databaseTables[i][1])
			
			generateRedemptionDB()
		else:
			print("Failed to created database!")
			print("Exiting Application...")
			sys.exit()
	
if __name__=="__main__":
	main()
