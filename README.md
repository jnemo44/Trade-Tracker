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

### User Types
Free User: Has access to all endpoints EXCEPT order-stats
Free User JWT:
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkR2WFFWOXNwZEFOQ2V1SUVpZ1dJaSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtNDQtMi5hdXRoMC5jb20vIiwic3ViIjoiQWtRVVRBUTBacXR6T205TlkxaEtmTnVLOHZqU3U1ZFFAY2xpZW50cyIsImF1ZCI6Im9yZGVycyIsImlhdCI6MTU5MTM3Mzg4NiwiZXhwIjoxNTkxNDYwMjg2LCJhenAiOiJBa1FVVEFRMFpxdHpPbTlOWTFoS2ZOdUs4dmpTdTVkUSIsInNjb3BlIjoiZ2V0OmNsb3NlLW9yZGVycyBnZXQ6b3Blbi1vcmRlcnMgcG9zdDpjbG9zZS1vcmRlciBwb3N0Om9wZW4tb3JkZXJzIHBhdGNoOm9wZW4tb3JkZXJzIHBhdGNoOmNsb3NlLW9yZGVycyBkZWxldGU6b3Blbi1vcmRlcnMgZGVsZXRlOmNsb3NlLW9yZGVycyIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbImdldDpjbG9zZS1vcmRlcnMiLCJnZXQ6b3Blbi1vcmRlcnMiLCJwb3N0OmNsb3NlLW9yZGVyIiwicG9zdDpvcGVuLW9yZGVycyIsInBhdGNoOm9wZW4tb3JkZXJzIiwicGF0Y2g6Y2xvc2Utb3JkZXJzIiwiZGVsZXRlOm9wZW4tb3JkZXJzIiwiZGVsZXRlOmNsb3NlLW9yZGVycyJdfQ.sjNKkQpG_pQtteM9lokVRA5cl876VXTJ1qOldFVuc0zdETCewQsga7Vego8f7K7RngW6H30j52zyy3bUWLow_N1XvSWI39r-A76kXI0dFntIMmiv76iRRz4yxdmfR6H8liRkNtu8kJvmCV5CU__xOuDtC6Tfl8NhdluMIie6Nf8bdrWRHV1qwjRTshEKulP5Ki_RqKWk5tWThmVE__0sUpKyE2uAI5z0hU1jvag0zsEeOUqm3L-GFFj6TI7gxEG62f9xPDVguWq5nMqqf8Ykg8j85MUlX8iZza9bqVVj6Y6Km1-fQ5C29S9AVyIiieWi3xPUHRIznwKQx8PCoUYEuA
```
Premium User: Has access to all endpoints
Premium User JWT:
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkR2WFFWOXNwZEFOQ2V1SUVpZ1dJaSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtNDQtMi5hdXRoMC5jb20vIiwic3ViIjoiQWtRVVRBUTBacXR6T205TlkxaEtmTnVLOHZqU3U1ZFFAY2xpZW50cyIsImF1ZCI6Im9yZGVycyIsImlhdCI6MTU5MTM3MzY4NCwiZXhwIjoxNTkxNDYwMDg0LCJhenAiOiJBa1FVVEFRMFpxdHpPbTlOWTFoS2ZOdUs4dmpTdTVkUSIsInNjb3BlIjoiZ2V0OmNsb3NlLW9yZGVycyBnZXQ6b3Blbi1vcmRlcnMgcG9zdDpjbG9zZS1vcmRlciBwb3N0Om9wZW4tb3JkZXJzIHBhdGNoOm9wZW4tb3JkZXJzIHBhdGNoOmNsb3NlLW9yZGVycyBkZWxldGU6b3Blbi1vcmRlcnMgZGVsZXRlOmNsb3NlLW9yZGVycyBnZXQ6b3JkZXItc3RhdHMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6Y2xvc2Utb3JkZXJzIiwiZ2V0Om9wZW4tb3JkZXJzIiwicG9zdDpjbG9zZS1vcmRlciIsInBvc3Q6b3Blbi1vcmRlcnMiLCJwYXRjaDpvcGVuLW9yZGVycyIsInBhdGNoOmNsb3NlLW9yZGVycyIsImRlbGV0ZTpvcGVuLW9yZGVycyIsImRlbGV0ZTpjbG9zZS1vcmRlcnMiLCJnZXQ6b3JkZXItc3RhdHMiXX0.ZMr2FEW6v88CjeO2SQrKNpmJr0psUwPHcuEZ4vHHfZVmbiFaCkl0bx5beOPqd1sywAg8SiqhlEXH7cCxWgvW8jp1d93AdiVXebdj9_IEITPk3HSmMgd74h3DBg66VpwL_S5YNac_kbUDEAmyPHbAfyc7Wek8t_E6BEiV7Kxtz1QiTkIqkDqHvc4R7K19m77xRIGyMx64o4nvtjkLQipd87ewKu7F-cUzso69-jHU4oyqiU3Q-y1ViwSqfhSWn3nmZwrX72tTlp8weXSlfhnwnSVL2Hb4knvRIO_UAhrSmaqBysH3KYJ1ylolsGS36CNId9rOfravgNjJpUwUcj9u3A
```

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
