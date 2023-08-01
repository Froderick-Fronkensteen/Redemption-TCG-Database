# Add in os support to check for files
import os

# Add in the pandas module for excel support
import pandas as pd

# Add in sqlite3 support
import sqlite3

# Database Connection Varaible
conn = None

# Checks to see if there is already a database file created
def doesDatabaseExist():
	return os.path.exists("redemption.db")

# Check to see if a specific database table exists
def doesTableExists(tableName):
	pass

# If there is no database found, then create one with all the correct tables
def createDatabaseConnection():
	# Variable to return whether database connectiom was created
	isDBConnectionCreated = False
	
	# Try to create the database connection, if the file doesn't exist it will be created
	try:
		global conn = sqlite3.connect("redemption.db")
		isDBConnectionCreated = True
		print(sqlite3.version)
	except Error as e:
		print(e)
	
	return databaseCreated

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

	# Read the specified excel file and store it
	excelFile = pd.ExcelFile('Redemption Card List.xlsx')
	
	# Read the Sets worksheet to get the name of every set
	setSheet = pd.read_excel(excelFile, 'Sets')
	
	setSheet = setSheet.reset_index()
	
	redemptionSets = []
	
	for index, row in setSheet.iterrows():
		redemptionSets.append([row[1], row[2].split('(')[0].strip(), row[2].split('(')[1].split(')')[0], row[3]])
	
	print(redemptionSets)
	
	# Read the specifice worksheet in the excel file and store it
	cardSheet = pd.read_excel(excelFile, 'Sets Card List')
	
	# Reset the index for the worksheet so it will start at 0
	cardSheet = cardSheet.reset_index()
	
	# Loop to iterate through all the rows
	for index, row in cardSheet.iterrows():
		print(row['Name'], row['#'], row['Set'], row['Type'], row['Brigade'], row['Strength'], row['Toughness'], row['Class'], row['Identifier'], row['Special Ability'], row['Rarity'], row['Book'], row['Chapter'], row['Verse'], row['Alignment'], row['Legality'], row['Artist'])

def main():

	print("Checking to see if redemption.db datbase exists...")

	# Check to see if database doesn't exist	
	if doesDatabaseExist() == False:
		# Redemption.db database was not found
		print("Database not found, creating database.")
		
		# Try to create the redemption.db database
		if createDatabaseConnection():
			print("Database was created successfully.")
		else:
			print("Failed to created database!")
	else:
		# Redemption.db database was found
		print("Redemption.db database was found, attempting to read Redemption Card List Excel file.")
		
		generateRedemptionDB()
	
if __name__=="__main__":
	main()
