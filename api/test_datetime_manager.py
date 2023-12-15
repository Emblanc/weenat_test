import pytest
from datetime import datetime
from datetime_manager import iso_to_timestamp, timestamp_to_iso

@pytest.mark.parametrize("ini_iso, final_ts", [
("2021-01-01T00:14:39+00:00", 1609460079000),
("2021-01-01T00:14:39-00:00", 1609460079000),
("2021-01-01T00:14:39", 1609460079000),
("2021-01-01T01:14:39+01:00", 1609460079000),
("2020-12-31T23:14:39-01:00", 1609460079000),
("2021-01-01T02:44:40+00:00", 1609469080000)
])

def test_iso_to_timestamp(ini_iso, final_ts):
	assert iso_to_timestamp(ini_iso) == final_ts


@pytest.mark.parametrize("iso_dt", [
"2021-01-01T00:14:39+00:00",
"2021-01-01T00:14:39-00:00", 
"2021-01-01T00:14:39", 
"2021-01-01T01:14:39+01:00", 
"2020-12-31T23:14:39-01:00"
])

def test_iso_to_iso(iso_dt):
	assert datetime.fromisoformat(timestamp_to_iso(iso_to_timestamp(iso_dt))) == datetime.fromisoformat("2021-01-01T00:14:39+00:00")


@pytest.mark.parametrize("ts_dt", [1609460079000, 1609469080000])

def test_ts_to_ts(ts_dt):
	assert iso_to_timestamp(timestamp_to_iso(ts_dt)) == ts_dt
