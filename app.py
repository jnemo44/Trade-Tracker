import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .database.models import setup_db, db_drop_and_create_all
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
  return jsonify ({
    'We are the champions':True
  })

@app.route('/close-orders', methods=['GET'])
def close_orders():
  return jsonify ({
    'Test':True
  })

@app.route('/order-stats', methods=['GET'])
@requires_auth('get:order-stats')
def order_stats():
  return jsonify ({
    'Test':True
  })

@app.route('/open-orders', methods=['POST'])
def new_open_order():
  return jsonify ({
    'Test':True
  })

@app.route('/close-orders', methods=['POST'])
def new_close_order():
  return jsonify ({
    'Test':True
  })

@app.route('/open-orders/<int:order_id>', methods=['PATCH'])
def edit_open_order(order_id):
  return jsonify ({
    'Test':True
  })

@app.route('/close-orders/<int:order_id>', methods=['PATCH'])
def edit_close_order(order_id):
  return jsonify ({
    'Test':True
  })

@app.route('/open-orders/<int:order_id>', methods=['DELETE'])
def delete_open_order(order_id):
  return jsonify ({
    'Test':True
  })

@app.route('/close-orders/<int:order_id>', methods=['DELETE'])
def delete_close_order(order_id):
  return jsonify ({
    'Test':True
  })

# Local Dev
if __name__ == '__main__':
  app.debug = True
  app.run()