"""
Script containing the functions to manage datetime formats.
"""

from datetime import datetime, timezone

def iso_to_timestamp(iso_date):
	dt = datetime.fromisoformat(iso_date)
	# If no timezone is specified, UTC is assumed
	if dt.tzinfo == None:
		dt_utc = dt.replace(tzinfo = timezone.utc)
	# If a timezone is specified, translation to UTC to match the timestamps in the db
	else:
		dt_utc = dt.astimezone(timezone.utc)
	return dt_utc.timestamp()*1000

def timestamp_to_iso(timestamp_date):
	return datetime.fromtimestamp(timestamp_date/1000, timezone.utc).isoformat()

