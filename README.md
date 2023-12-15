# Test BackEnd Weenat

Author : Emmanuelle Blanc

## Requirements

See requirements.txt

## Authentification

The database created and accessed through the API is a mySQL database (mySQL is thus required).
To be able to create and access the mySQL  database, a config.py file must be present in the api and database_creation directories.
An example file is provided. This file must be updated by the user to contain their user id and password for mysql.

## Use

### Database creation
MySQL is required.
Make sure that the initial data is available at "http://localhost:3000/measurements" or change the url in database_creation/main.py to indicate the right url.
See "Authentification".
In the databse_creation/ directory :
`python3 main.py`

### API
Once the mySQL database is created.
In the api/ directory :
`python3 api.py`

## Choices description

### dataloggerParam
The API uses a required dataloggerParam parameter that must be an exact match of the datalogger id.
Since no datalogger id were provided in the data, datalogger id were created as datalogger0001 and datalogger0002.

### Timestamp management
Timestamps provided in the data were assumed to be in Unix time milliseconds.
All date and time management is made using UTC to avoid any discrepancy between users based on their location.
