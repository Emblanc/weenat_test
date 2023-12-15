"""
Script to setup the API.
"""
import uvicorn
import pandas as pd
from datetime import datetime, timezone
from fastapi import FastAPI, Query, HTTPException
from datetime_manager import iso_to_timestamp, timestamp_to_iso
from api_utils import fetch_raw_data, format_output_data, aggregate_raw_data, spanEnum

app = FastAPI()

@app.get("/api/data", responses = {200: {"description": "Array of records matching the input criteria"}, 400: {"description": "Missing required values"}})
def api_fetch_data_raw(
dataloggerParam: str = Query(title = "datalogger", description = "Filter by datalogger. Should be an exact match of the datalogger id (datalogger0001 or datalogger0002)"),
sinceParam: str = Query(default = "1970-01-01T00:00:00+00:00", title = "since", description = "Filter by date and time. Only returns data measured strictly after this date and time. Expected format : ISO-8601 UTC+00:00. Parameters given with another timezone will be translated to UTC. Parameters given without specifying the timezone will be assumed to be in UTC."),
beforeParam: str = Query(default = datetime.now(timezone.utc).isoformat(), title = "before", description = "Filter by date and time. Only returns data measured strictly before this date and time. Expected format : ISO-8601 UTC+00:00. Parameters given with another timezone will be translated to UTC. Parameters given without specifying the timezone will be assumed to be in UTC.")
):
	"""
	Endpoint to return the data stored. The output is the raw data stored.
	"""
	if not dataloggerParam:
		raise HTTPException(status_code=400, detail="Missing required values")
	raw_data = fetch_raw_data(dataloggerParam, sinceParam, beforeParam)
	raw_data_json = format_output_data(raw_data)
	return raw_data_json


@app.get("/api/summary", responses = {200: {"description": "Array of records matching the input criteria"}})
def api_fetch_data_aggregates(
dataloggerParam: str = Query(title = "datalogger", description = "Filter by datalogger. Should be an exact match of the datalogger id (datalogger0001 or datalogger0002)"),
sinceParam: str = Query(default = "1970-01-01T00:00:00+00:00", title = "since", description = "Filter by date and time. Only returns data measured strictly after this date and time. Expected format : ISO-8601 UTC+00:00. Parameters given with another timezone will be translated to UTC. Parameters given without specifying the timezone will be assumed to be in UTC."),
beforeParam: str = Query(default = datetime.now(timezone.utc).isoformat(), title = "before", description = "Filter by date and time. Only returns data measured strictly before this date and time. Expected format : ISO-8601 UTC+00:00.  Parameters given with another timezone will be translated to UTC. Parameters given without specifying the timezone will be assumed to be in UTC."),
spanParam: spanEnum = Query(default = spanEnum.raw, title = "span", description = "Aggregates data given this parameter. Max returns raw data."),
):
	"""
	Endpoint to return aggregates of the data stored.
	For temp and hum, results are mean, min and max.
	For precip, result is the sum.
	"""
	raw_data = fetch_raw_data(dataloggerParam, sinceParam, beforeParam)
	if raw_data == []:
		return raw_data
	else:
		if spanParam == "max":
			agg_data_json = format_output_data(raw_data)
		elif spanParam == "day" or spanParam == "hour":
			raw_data_df = pd.DataFrame(raw_data, columns = ["timestamp", "precip", "temp", "hum"])
			agg_data_json = aggregate_raw_data(raw_data_df, spanParam[0].upper())
		return agg_data_json


if __name__ == "__main__":
	uvicorn.run(app, host="localhost", port=8000)
