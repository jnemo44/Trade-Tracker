import os
import decimal
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .database.models import setup_db, db_drop_and_create_all, Open, Close, db
from .auth.auth import AuthError, requires_auth


# Create application
app = Flask(__name__)
setup_db(app)
CORS(app)

#db_drop_and_create_all()

'''
# Hosted deployment
if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
'''
@app.route('/open-orders', methods=['GET'])
def open_orders():
  available_orders = Open.query.all()
  current_trades = [orders.opening_trade() for orders in available_orders]
  
  return jsonify ({
    'success':True,
    'open_list':current_trades
  })

@app.route('/close-orders', methods=['GET'])
def close_orders():
  available_orders = Close.query.all()
  current_trades = [orders.closing_trade() for orders in available_orders]

  return jsonify ({
    'success':True,
    'close_list':current_trades
  })

@app.route('/order-stats', methods=['GET'])
#@requires_auth('get:order-stats')
def order_stats():
  num_opened = 0
  totals = {}
  total_profit = 0

  # Retrieve all records (Is this necessary?)
  open_orders = Open.query.all()
  close_orders = Close.query.all()

  while num_opened < len(open_orders):
    close_price = db.session.query(Close.close_price, Close.number_contracts).filter(Close.open_id==open_orders[num_opened].id).all()    
    ticker_profit = open_orders[num_opened].open_price
    # For every open trade subtract cost of closing trade
    for cost in close_price:
      # The number of contracts closed serves as a multiplier
      contracts_closed = close_price[0][1]
      if open_orders[num_opened].buy_sell == 'sell':
        ticker_profit -= cost[0] * contracts_closed
      else:
        ticker_profit += cost[0] * contracts_closed
    #Convert decimal to a str for JSON
    totals[open_orders[num_opened].ticker] = str(ticker_profit)
    num_opened+=1

  # Calculate total profit
  for v in totals.values():
    total_profit += float(v)

  return jsonify ({
    'success':True,
    'open_orders':len(open_orders),
    'close_orders':len(close_orders),
    'ticker_profit':totals,
    'total_profit':str(round(total_profit,2))

  })

@app.route('/open-orders', methods=['POST'])
def new_open_order():
  return jsonify ({
    'success':True
  })

@app.route('/close-orders', methods=['POST'])
def new_close_order():
  return jsonify ({
    'success':True
  })

@app.route('/open-orders/<int:order_id>', methods=['PATCH'])
def edit_open_order(order_id):
  return jsonify ({
    'success':True
  })

@app.route('/close-orders/<int:order_id>', methods=['PATCH'])
def edit_close_order(order_id):
  return jsonify ({
    'success':True
  })

@app.route('/open-orders/<int:order_id>', methods=['DELETE'])
def delete_open_order(order_id):
  return jsonify ({
    'success':True
  })

@app.route('/close-orders/<int:order_id>', methods=['DELETE'])
def delete_close_order(order_id):
  return jsonify ({
    'success':True
  })

# Local Dev
if __name__ == '__main__':
  app.debug = True
  app.run()