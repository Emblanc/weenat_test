"""
Script to load the measurement data from the initial database.
"""

import requests
import pandas as pd

def fetch_data(api_url):
	"""
	Function to fetch data from an API endpoint.
	
	Parameters
	----------
	api_url (str) : url to access the data
	
	Returns
	-------
	list or dict : the JSON data retrived from the API or None if the request was unsuccessful
	
	"""
	response = requests.get(api_url)
	if response.status_code == 200:
		return response.json()
	else:
		print("Error status code " + str(response.status_code))

