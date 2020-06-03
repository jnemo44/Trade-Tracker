# Trade-Tracker 
## A tool for tracking your options trading portfolio
This tool was born out of my personal desire to have a simple tool for keeping track of my options trading investment portfolio. I needed something to quickly and accuratly track open and closed trades while also calculating some key metrics to help me better understand my portfolio. It is still a work in progress, but over time I hope to implement a front end to compliment what is currently only a backend service.

## Getting Started

### Required Dependancies
* Python 3.7
* Postgres (required for local dev)
* Virtual Environment
* PIP Dependencies
After activating the virtual environment run `pip install -r requirements.txt` to install python package dependencies for this project.

### Create the Database
For local development a database named trade_tracker is used. Using a tool like PgAdmin4 create that database ensuring the correct path is declared in models.py

### Run the Flask Server
Inside the trade_tracker top level folder run the following commands to start the flask server. The FLASK_APP and FLASK_ENV commands are only required on first run.
#### Windows PS
`$ENV:FLASK_APP = 'flaskr'`
`$ENV:FLASK_ENV = 'development'`
`flask run`
#### Bash
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
### Add Dummy Data to Database
After starting the flask server for the first time the tables will now exsist in your trade_tracker database. You can now use a tool like PgAdmin4 to insert the dummy trade data found in the dummydata file.

### Tests
In order to run endpoint tests you need to run the following commands in a SQL Shell.

```
DROP DATABASE trade_tracker_test (ommit if first time running tests)
CREATE DATABASE trade_tracker_test
```
Then you can run the test file with a normal terminal from the trade_tracker directory. 
```
python test_app.py
``` 

## API Reference
### Getting Started
Base URL (Local Dev): `http://127.0.0.1:5000/`
Hosted URL: `TBD`

### Error Handling
Standard HTTP response codes used.
```
{
    'success':False,
    'error':404,
    'message':'Resource not found!'
}
```

The current API returns the following codes as JSON objects.

* 400 - Bad Request from client
* 404 - Resource not found
* 422 - Unprocessable

### Endpoint Library

#### GET `/open-orders`
Returns a list of all open orders

#### GET `/close-orders`
Returns a list of all close orders

#### GET `/order-stats`
Based on your open and close orders this endpoint returns a few simple stats about your trade history.

#### POST `/open-orders`
Add a new open order using the following parameters in your request.

#### POST `/close-orders`
Add a new close order using the following parameters in your request.

#### PATCH `/open-orders/<int:order_id>`
This endpoint allows you to change only the open order description. The patch request expects a JSON object containing a new order description.

#### PATCH `/close-orders/<int:order_id>`
This endpoint allows you to change only the close order description. The patch request expects a JSON object containing a new order description.

#### DELETE `/open-orders/<int:order_id>`
A delete request will cascade, by also deleting any close orders associated with the open-order being deleted. This ensures that no orphans are left in the close-orders table.

## Author
Me. jnemo44. aka Joe N.

## Acknowledgments
This porject was based on information taught by Udacity in their Full Stack Web Dev course and serves as my capstone project.
