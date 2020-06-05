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
```
$ENV:FLASK_APP = 'flaskr'
$ENV:FLASK_ENV = 'development'
flask run
```
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
Hosted URL: `https://trade-tracker-tool.herokuapp.com/`

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
`curl https://trade-tracker-tool.herokuapp.com/open-orders`

Returns:
```
{
  "open_list": [
    {
      "adjustment": false,
      "buy_sell": "sell",
      "id": 1,
      "number_contracts": 1,
      "open_date": "Mon, 25 May 2020 00:00:00 GMT",
      "open_description": "Testing out the strategy",
      "open_price": "2.34",
      "ticker": "EEM",
      "trade_type": "Iron Butterfly"
    },
    {
      "adjustment": false,
      "buy_sell": "sell",
      "id": 2,
      "number_contracts": 1,
      "open_date": "Mon, 25 May 2020 00:00:00 GMT",
      "open_description": "Testing out the strategy",
      "open_price": "3.04",
      "ticker": "FXI",
      "trade_type": "Iron Butterfly"
    },
    {
      "adjustment": false,
      "buy_sell": "sell",
      "id": 3,
      "number_contracts": 1,
      "open_date": "Mon, 25 May 2020 00:00:00 GMT",
      "open_description": "Testing out the strategy",
      "open_price": "2.56",
      "ticker": "XOP",
      "trade_type": "Iron Butterfly"
    },
    {
      "adjustment": false,
      "buy_sell": "sell",
      "id": 4,
      "number_contracts": 1,
      "open_date": "Mon, 25 May 2020 00:00:00 GMT",
      "open_description": "Testing out the strategy",
      "open_price": "1.00",
      "ticker": "XBI",
      "trade_type": "Iron Butterfly"
    }
  ],
  "success": true
}
```

#### GET `/close-orders`
Returns a list of all close orders
`curl https://trade-tracker-tool.herokuapp.com/open-orders`

Returns:
```
{
  "close_list": [
    {
      "adjustment": false,
      "buy_sell": "buy",
      "close_date": "Mon, 25 May 2020 00:00:00 GMT",
      "close_description": "Testing out the strategy",
      "close_price": "0.87",
      "id": 1,
      "number_contracts": 1,
      "open_id": 1
    },
    {
      "adjustment": false,
      "buy_sell": "buy",
      "close_date": "Mon, 25 May 2020 00:00:00 GMT",
      "close_description": "Testing out the strategy",
      "close_price": "1.01",
      "id": 2,
      "number_contracts": 1,
      "open_id": 2
    },
    {
      "adjustment": false,
      "buy_sell": "buy",
      "close_date": "Mon, 25 May 2020 00:00:00 GMT",
      "close_description": "Testing out the strategy",
      "close_price": "0.54",
      "id": 3,
      "number_contracts": 1,
      "open_id": 3
    },
    {
      "adjustment": false,
      "buy_sell": "buy",
      "close_date": "Mon, 25 May 2020 00:00:00 GMT",
      "close_description": "Testing out the strategy",
      "close_price": "3.00",
      "id": 4,
      "number_contracts": 1,
      "open_id": 4
    }
  ],
  "success": true
}
```

#### GET `/order-stats`
Based on your open and close orders this endpoint returns a few simple stats about your trade history.
`curl https://trade-tracker-tool.herokuapp.com/order-stats`

Returns:
```
{
  "close_orders": 4,
  "open_orders": 5,
  "success": true,
  "ticker_profit": {
    "EEM": "1.47",
    "FXI": "2.03",
    "GPS": "1.75",
    "XBI": "-2.00",
    "XOP": "2.02"
  },
  "total_profit": "5.27"
}
```

#### POST `/open-orders`
Add a new open order using the following parameters in your request.
```
curl -X POST https://trade-tracker-tool.herokuapp.com/open-orders -H "Content-Type: application/json" -d '{
	"open_date":"5/26/2020",
	"buy_sell":"sell",
	"ticker":"GPS",
	"number_contracts":3,
	"open_price":4.75,
	"adjustment":false,
	"trade_type":"Iron Condor",
	"open_description":"Open Description"
}'
```
Returns:
```
{
  "current_trades": [
    {
      "adjustment": false,
      "buy_sell": "sell",
      "id": 1,
      "number_contracts": 1,
      "open_date": "Mon, 25 May 2020 00:00:00 GMT",
      "open_description": "Testing out the strategy",
      "open_price": "2.34",
      "ticker": "EEM",
      "trade_type": "Iron Butterfly"
    },
    {
      "adjustment": false,
      "buy_sell": "sell",
      "id": 2,
      "number_contracts": 1,
      "open_date": "Mon, 25 May 2020 00:00:00 GMT",
      "open_description": "Testing out the strategy",
      "open_price": "3.04",
      "ticker": "FXI",
      "trade_type": "Iron Butterfly"
    },
    {
      "adjustment": false,
      "buy_sell": "sell",
      "id": 3,
      "number_contracts": 1,
      "open_date": "Mon, 25 May 2020 00:00:00 GMT",
      "open_description": "Testing out the strategy",
      "open_price": "2.56",
      "ticker": "XOP",
      "trade_type": "Iron Butterfly"
    },
    {
      "adjustment": false,
      "buy_sell": "sell",
      "id": 4,
      "number_contracts": 1,
      "open_date": "Mon, 25 May 2020 00:00:00 GMT",
      "open_description": "Testing out the strategy",
      "open_price": "1.00",
      "ticker": "XBI",
      "trade_type": "Iron Butterfly"
    },
    {
      "adjustment": false,
      "buy_sell": "sell",
      "id": 5,
      "number_contracts": 3,
      "open_date": "Tue, 26 May 2020 00:00:00 GMT",
      "open_description": "Open Description",
      "open_price": "4.75",
      "ticker": "GPS",
      "trade_type": "Iron Condor"
    }
  ],
  "success": true
}
```
#### POST `/close-orders`
Add a new close order using the following parameters in your request.
```
curl -X POST https://trade-tracker-tool.herokuapp.com/close-orders -H "Content-Type: application/json" -d '{
	"open_id":5,
	"close_date":"5/26/2020",
	"buy_sell":"buy",
	"number_contracts":3,
	"close_price":2.84,
	"adjustment":false,
	"close_description":"Close description"
}' 
```
Returns:
```
{
  "close_list": [
    {
      "adjustment": false,
      "buy_sell": "buy",
      "close_date": "Mon, 25 May 2020 00:00:00 GMT",
      "close_description": "Testing out the strategy",
      "close_price": "0.87",
      "id": 1,
      "number_contracts": 1,
      "open_id": 1
    },
    {
      "adjustment": false,
      "buy_sell": "buy",
      "close_date": "Mon, 25 May 2020 00:00:00 GMT",
      "close_description": "Testing out the strategy",
      "close_price": "1.01",
      "id": 2,
      "number_contracts": 1,
      "open_id": 2
    },
    {
      "adjustment": false,
      "buy_sell": "buy",
      "close_date": "Mon, 25 May 2020 00:00:00 GMT",
      "close_description": "Testing out the strategy",
      "close_price": "0.54",
      "id": 3,
      "number_contracts": 1,
      "open_id": 3
    },
    {
      "adjustment": false,
      "buy_sell": "buy",
      "close_date": "Mon, 25 May 2020 00:00:00 GMT",
      "close_description": "Testing out the strategy",
      "close_price": "3.00",
      "id": 4,
      "number_contracts": 1,
      "open_id": 4
    }
  ],
  "success": true
}
```

#### PATCH `/open-orders/<int:order_id>`
This endpoint allows you to change only the open order description. The patch request expects a JSON object containing a new order description.
`curl -X PATCH https://trade-tracker-tool.herokuapp.com/open-orders/1 -H "Content-Type: application/json" -d '{"open_description":"This i
s a new description"}'`

Returns:
```
{
  "new_description": "This is a new description",
  "success": true,
  "updated_order_id": 1
}
```

#### PATCH `/close-orders/<int:order_id>`
This endpoint allows you to change only the close order description. The patch request expects a JSON object containing a new order description.
`curl -X PATCH https://trade-tracker-tool.herokuapp.com/close-orders/1 -H "Content-Type: application/json" -d '{"open_description":"This
is a new description"}'`

Returns:
```
{
  "new_description": "This is a new description",
  "success": true,
  "updated_order_id": 1
}
```

#### DELETE `/open-orders/<int:order_id>`
A delete request will cascade, by also deleting any close orders associated with the open-order being deleted. This ensures that no orphans are left in the close-orders table.
`curl -X DELETE https://trade-tracker-tool.herokuapp.com/open-orders/1`

Returns:
```
{
  "deleted_id": 1,
  "success": true
}
```

## Author
Me. jnemo44. aka Joe N.

## Acknowledgments
This porject was based on information taught by Udacity in their Full Stack Web Dev course and serves as my capstone project.
