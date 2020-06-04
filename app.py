import os
import decimal
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from database.models import setup_db, db_drop_and_create_all, Open, Close, db
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):
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
    #Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        #response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

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

        # If no orders exsist abort
        if len(open_orders) == 0:
            abort(404)
        elif len(close_orders) == 0:
            abort(404)
        try:
            # Go through every open order and find coresponding close orders
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
            for price in totals.values():
                total_profit += float(price)

            return jsonify ({
                'success':True,
                'open_orders':len(open_orders),
                'close_orders':len(close_orders),
                'ticker_profit':totals,
                'total_profit':str(round(total_profit,2))

            })
        except:
            abort(422)

    @app.route('/open-orders', methods=['POST'])
    def new_open_order():
        body = request.get_json()
        new_date = body.get('open_date',None)
        new_buy_sell = body.get('buy_sell',None)
        new_ticker = body.get('ticker',None)
        new_contracts = body.get('number_contracts',None)
        new_price = body.get('open_price',None)
        new_adjustment = body.get('adjustment',None)
        new_type = body.get('trade_type',None)
        new_description = body.get('open_description',None)

        if new_date is None:
            abort(400)

        try:
            new_trade = Open(
            open_date=new_date,
            buy_sell=new_buy_sell,
            ticker=new_ticker,
            number_contracts=new_contracts,
            open_price=new_price,
            adjustment=new_adjustment,
            trade_type=new_type,
            open_description=new_description
            )

            # Add new model to the database
            new_trade.insert()

            available_orders = Open.query.all()
            current_trades = [orders.opening_trade() for orders in available_orders] 

            return jsonify ({
            'success':True,
            'current_trades':current_trades
            })
        except:
            abort(422)

    @app.route('/close-orders', methods=['POST'])
    def new_close_order():
        body = request.get_json()
        new_oid = body.get('open_id',None)
        new_date = body.get('close_date',None)
        new_buy_sell = body.get('buy_sell',None)
        new_contracts = body.get('number_contracts',None)
        new_price = body.get('close_price',None)
        new_adjustment = body.get('adjustment',None)
        new_description = body.get('close_description',None)

        try:
            new_trade = Close(
            open_id = new_oid,
            close_date = new_date,
            buy_sell = new_buy_sell,
            number_contracts = new_contracts,
            close_price = new_price,
            adjustment = new_adjustment,
            close_description = new_description
            )

            new_trade.insert()

            available_orders = Close.query.all()
            current_trades = [orders.closing_trade() for orders in available_orders]

            return jsonify ({
            'success':True,
            'close_orders':current_trades
            })
        except:
            abort(422)

    @app.route('/open-orders/<int:order_id>', methods=['PATCH'])
    def edit_open_order(order_id):
        selected_order = Open.query.filter(Open.id == order_id).one_or_none()

        # Order not found
        if selected_order is None:
            abort(404)
        
        body = request.get_json()
        # Currently only allow updating the description
        new_description = body.get('open_description',None)

        # Bad Request
        if new_description is None:
            abort(400)

        try:
            # Push update to database
            selected_order.open_description = new_description
            selected_order.update()

            return jsonify ({
            'success':True,
            'updated_order_id':order_id,
            'new_description':new_description
            })
        
        except:
            abort(422)

    @app.route('/close-orders/<int:order_id>', methods=['PATCH'])
    def edit_close_order(order_id):
        selected_order = Close.query.filter(Close.id == order_id).one_or_none()

        # Order not found
        if selected_order is None:
            abort(404)
        
        body = request.get_json()
        # Currently only allow updating the description
        new_description = body.get('close_description',None)

        # Bad Request
        if new_description is None:
            abort(400)

        try:
            # Push update to database
            selected_order.close_description = new_description
            selected_order.update()

            return jsonify ({
            'success':True,
            'updated_order_id':order_id,
            'new_description':new_description
            })

        except:
            abort(422)

    @app.route('/open-orders/<int:order_id>', methods=['DELETE'])
    def delete_open_order(order_id):
        # Deleting an open order will delete all matching closing orders
        selected_order = Open.query.filter(Open.id == order_id).one_or_none()

        # Nothing to delete
        if selected_order is None:
            abort(404)

        try:
            selected_order.delete()

            return jsonify ({
            'success':True,
            'deleted_id':order_id
            })

        except:
            abort(422)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success':False,
            'error':400,
            'message':'Bad Request'
        }),400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success':False,
            'error':404,
            'message':'Resource not found!'
        }),404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success':False,
            'error':422,
            'message':'Unprocessable'
        }),422

    @app.errorhandler(AuthError)
    def authorization_error(error):
        return jsonify({
            "success": False, 
            "error": error.status_code,
            "message": error.error['code']
        }), error.status_code


    return app
    # Local Dev
    #if __name__ == '__main__':
    #app.debug = True
    #app.run()