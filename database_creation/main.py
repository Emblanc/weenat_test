from data_fetcher import fetch_data
from db_creator import create_db_tables

measurements_url = "http://localhost:3000/measurements"

fetched_data = fetch_data(measurements_url)

create_db_tables(data = fetched_data)
