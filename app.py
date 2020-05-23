import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db 



#def create_app(test_config=None):
  # create and configure the app
app = Flask(__name__)
setup_db(app)
CORS(app)

#APP = create_app()

'''
# Hosted deployment
if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
'''
@app.route('/open-orders', methods=['GET'])
def home_page():
  return jsonify ({
    'We are the champions':True
  })

@app.route('/close-orders', methods=['GET'])
def close_orders():
  return jsonify ({
    'Test':True
  })

@app.route('/open-orders/<int:order_id>', methods=['PATCH'])
def edit_open_orders(order_id):
  return jsonify ({
    'Test':True
  })

@app.route('/close-orders/<int:order_id>', methods=['PATCH'])
def edit_close_orders(order_id):
  return jsonify ({
    'Test':True
  })

# Local Dev
if __name__ == '__main__':
  app.debug = True
  app.run()