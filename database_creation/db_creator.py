"""
Script to create the database
"""

import mysql.connector
from config import DB_CONFIG

def create_db_tables(data: list, db_config: dict = DB_CONFIG, db_name: str = "measurements"):
	"""
	Function to create the database and 1 table for each datalogger
	Parameters
	----------
	data (list) : a list of dict containing the measurement data
	db_config (dict) : dictionnary containing user, host and password for the connection to mySQL. Defaut = DB_CONFIG which should be imported from a config.py file.
	db_name (str) : name of the database to create. Default = "measurements"
	"""
	with mysql.connector.connect(user = db_config["user"], host = db_config["host"], password = db_config["password"]) as db_connection:
		with db_connection.cursor() as db_cursor:
		# Opening connection to mySQL using a with statement to ensure
		# the connection and cursor are properly closed, even in the case 
		# of an Exception
			# Check if the db already exists
			db_cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
			if db_cursor.fetchone():
				print(f"Database '{db_name}' already exists. Exiting script.")
				exit()
			# Proceed with the creation of the db if it doesn't already exist
			else:
				db_cursor.execute(f"CREATE DATABASE {db_name}")
				db_cursor.execute(f"USE {db_name}")
				for datalogger_idx, datalogger_data in enumerate(data):
					datalogger_name = f"datalogger{(datalogger_idx+1):04d}"
					db_cursor.execute(f"CREATE TABLE {datalogger_name} (timestamp BIGINT PRIMARY KEY, precip FLOAT, temp FLOAT, hum FLOAT)")
					for timestamp, measures in datalogger_data.items():
						db_cursor.execute(f"INSERT INTO {datalogger_name} (timestamp, precip, temp, hum) VALUES (%s, %s, %s, %s)", [timestamp, measures['precip'], measures['temp'], measures['hum']])
				db_connection.commit()

