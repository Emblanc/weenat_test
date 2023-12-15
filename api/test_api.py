import pytest
from fastapi.testclient import TestClient
from api import app

@pytest.fixture
def client():
	return TestClient(app)

# Testing each endpoint separately to help identify any issue.

def test_empty_data(client):
	response = client.get("/api/data?dataloggerParam=datalogger0001&sinceParam=2023-12-01T00%3A00%3A00%2B00%3A00&beforeParam=2023-12-10T00%3A00%3A00%2B00%3A00")
	assert response.status_code == 200
	assert response.json() == []

@pytest.mark.parametrize("api_url_empty", [
"/api/summary?dataloggerParam=datalogger0001&sinceParam=2023-12-01T00%3A00%3A00%2B00%3A00&beforeParam=2023-12-10T00%3A00%3A00%2B00%3A00&spanParam=hour",
"/api/summary?dataloggerParam=datalogger0001&sinceParam=2023-12-01T00%3A00%3A00%2B00%3A00&beforeParam=2023-12-10T00%3A00%3A00%2B00%3A00&spanParam=day",
"/api/summary?dataloggerParam=datalogger0001&sinceParam=2023-12-01T00%3A00%3A00%2B00%3A00&beforeParam=2023-12-10T00%3A00%3A00%2B00%3A00&spanParam=max",
"/api/summary?dataloggerParam=datalogger0001&sinceParam=2023-12-01T00%3A00%3A00%2B00%3A00&beforeParam=2023-12-10T00%3A00%3A00%2B00%3A00"
])
def test_empty_summary(client, api_url_empty):
	response = client.get(api_url_empty)
	assert response.status_code == 200
	assert response.json() == []



def test_na_data(client):
	response = client.get("/api/data?dataloggerParam=datalogger0002&sinceParam=2021-09-11T08%3A00%3A00%2B00%3A00&beforeParam=2021-09-11T09%3A00%3A00%2B00%3A00")
	assert response.status_code == 200

@pytest.mark.parametrize("api_url_na", [
"/api/summary?dataloggerParam=datalogger0002&sinceParam=2021-09-11T08%3A00%3A00%2B00%3A00&beforeParam=2021-09-11T09%3A00%3A00%2B00%3A00&spanParam=max",
"/api/summary?dataloggerParam=datalogger0002&sinceParam=2021-09-11T08%3A00%3A00%2B00%3A00&beforeParam=2021-09-11T09%3A00%3A00%2B00%3A00&spanParam=day",
"/api/summary?dataloggerParam=datalogger0002&sinceParam=2021-09-11T08%3A00%3A00%2B00%3A00&beforeParam=2021-09-11T09%3A00%3A00%2B00%3A00&spanParam=hour"
])
def test_na_summary(client, api_url_na):
	response = client.get(api_url_na)
	assert response.status_code == 200

@pytest.mark.parametrize("api_url_length, output_length", [
("/api/summary?dataloggerParam=datalogger0002&sinceParam=2021-09-11T08%3A00%3A00%2B00%3A00&beforeParam=2021-09-11T10%3A00%3A00%2B00%3A00&spanParam=day", 7),
("/api/summary?dataloggerParam=datalogger0002&sinceParam=2021-09-11T08%3A00%3A00%2B00%3A00&beforeParam=2021-09-11T10%3A00%3A00%2B00%3A00&spanParam=hour", 14)
])
def test_length_summary(client, api_url_length, output_length):
	response = client.get(api_url_length)
	assert response.status_code == 200
	assert len(response.json()) == output_length
