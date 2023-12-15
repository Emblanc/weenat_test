"""
Script containing useful classes and functions for the API.
"""
from enum import Enum
from datetime import datetime, timezone
import mysql.connector
import pandas as pd
import json
from datetime_manager import iso_to_timestamp, timestamp_to_iso
from config import DB_CONFIG

class spanEnum(str, Enum):
	day = "day"
	hour = "hour"
	raw = "max"

def format_output_data(data):
	"""
	Function to format the data retrived from the db.
	Parameters:
	----------
	data (list) : data retrived from the db
	Returns:
	-------
	list of dict
	"""
	data_df = pd.DataFrame(data, columns = ["timestamp", "precip", "temp", "hum"])
	melted_df = pd.melt(data_df, id_vars=["timestamp"], var_name = "label", value_name = "value")
	# Time format is changed to ISO and placed between label and value to match the output format
	melted_df["measured_at"] = melted_df["timestamp"].apply(timestamp_to_iso)
	melted_df = melted_df[["label", "measured_at", "value"]]
	# Changing the Nas to None for the conversion to json
	melted_df = melted_df.where(melted_df.notna(), None)
	json_output = melted_df.to_dict(orient = "records")
	return json_output

def fetch_raw_data(datalogger: str, since: str, before: str):
	"""
	Function to fetch the raw data stored in the db.
	Parameters:
	----------
	datalogger (str): Datalogger id
	since (str) : Filter by date and time. Only returns data measured strictly after this date and time. Expected format : ISO-8601 UTC+00:00.
	before (str) : Filter by date and time. Only returns data measured strictly before this date and time. Expected format : ISO-8601 UTC+00:00.
	"""
	since_ts = iso_to_timestamp(since)
	before_ts = iso_to_timestamp(before)
	with mysql.connector.connect(user = DB_CONFIG["user"], host = DB_CONFIG["host"], password = DB_CONFIG["password"], database = "measurements") as db_connection:
		with db_connection.cursor() as db_cursor:
			db_cursor.execute(f"SELECT timestamp, precip, temp, hum FROM {datalogger} WHERE timestamp < %s AND timestamp > %s", [before_ts, since_ts])
			return db_cursor.fetchall()

def aggregate_raw_data(raw_df, agg_span):
	"""
	Function to aggregate data.
	Parameters:
	----------
	raw_df (pd.DataFrame) : raw data with 1 row for each timestamp and 1 column for each measure
	agg_span (str) : Aggregation based on this parameter. Either "D" for day or "H" for hour
	Returns: 
	-------
	list of dict with the corresponding aggregates (mean for temp and hum, sum for precip)
	"""
	# Changing timestamp to datetime
	raw_df["dt"] = raw_df["timestamp"].apply(lambda x: datetime.fromtimestamp(x/1000, timezone.utc))
	# Aggregating data
	agg_df = raw_df.groupby(raw_df["dt"].dt.floor(agg_span)).agg({"precip": "sum", "temp": ["mean", "min", "max"], "hum": ["mean", "min", "max"]}).reset_index()
	# Flatten the multi index columns
	agg_df.columns = ["_".join(col).rstrip("_") for col in agg_df.columns.values]
	# Changing data format to match expectetions
	melted_agg_df = pd.melt(agg_df, id_vars = ["dt"], var_name = "label", value_name = "value")
	# Time format is changed to ISO and placed between label and value to match the output format
	melted_agg_df["time_slot"] = melted_agg_df["dt"].apply(lambda x: x.isoformat())
	melted_agg_df = melted_agg_df[["label", "time_slot", "value"]]
	# Changing the Nas to None for the conversion to json
	melted_agg_df = melted_agg_df.where(melted_agg_df.notna(), None)
	agg_data_json = melted_agg_df.to_dict(orient = "records")
	return agg_data_json


