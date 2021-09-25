import os
import sys
import decimal
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.sql.expression import false, distinct
from database.models import (
    setup_db,
    db_drop_and_create_all,
    Open,
    Close,
    db
)
from auth.auth import AuthError, requires_auth
from flask_migrate import Migrate


def create_app(test_config=None):
    # Create application
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # Command used to reset database tables
    #db_drop_and_create_all()

    # Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS')
        #response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            'message': 'Welcome to the trade tracker tool!'
        })

    @app.route('/logout', methods=['GET'])
    def logout():
        return jsonify({
            'logout': True
        })

    @app.route('/open-orders', methods=['GET'])
    #@requires_auth('get:open-orders')
    def open_orders():
        open_adjusted_trade_IDs = []
        open_adjusted_orders = []
        open_adjusted_trades = []

        # Get all open orders (no open adjustments)
        available_orders = Open.query.filter(Open.closed == 'false').all()
        current_trades = [orders.opening_trade()
                          for orders in available_orders]

        # Get all Adjustment ID's that exist
        unique_id = db.session.query(distinct(Open.adjustment_id)).all()
        # Extract just the id from the list of tuples and removing None if present
        unique_id_list = list(filter(None, [id[0] for id in unique_id]))
        # Split all adjustment ID's into open and closed
        adjusted_trade_IDs = Open.open_adjustment_list(unique_id_list)
        # Index 0 contains closed adjustments Index 1 contains open adjustments
        open_adjusted_trade_IDs = adjusted_trade_IDs[1]

        # Get adjusted close orders
        for idx, id in enumerate(open_adjusted_trade_IDs):
            # Do some query that returns the combined info of a series of adjustments
            open_adjusted_orders.append(db.session.query(Open, Close).filter(Close.adjustment_id == id).join(Close).all())
            open_adjusted_trades.append([{**open.opening_trade(), **close.closing_trade()}
                          for open, close in open_adjusted_orders[idx]])

        return jsonify({
            'success': True,
            'open_list': current_trades,
            'open_adjusted_trades': open_adjusted_trades
        })

    @app.route('/close-orders', methods=['GET'])
    #@requires_auth('get:close-orders')
    def close_orders():
        closed_adjusted_orders = []
        closed_adjusted_trades = []

        # Get all Adjustment ID's that exist
        unique_id = db.session.query(distinct(Open.adjustment_id)).all()
        # Extract just the id from the list of tuples and removing None if present
        unique_id_list = list(filter(None, [id[0] for id in unique_id]))

        # Split all adjustment ID's into open and closed
        adjusted_trade_IDs = Open.open_adjustment_list(unique_id_list)
        # Index 0 contains closed adjustments Index 1 contains open adjustments
        closed_adjusted_trade_IDs = adjusted_trade_IDs[0]
        
        # Get adjusted close orders
        for idx, id in enumerate(closed_adjusted_trade_IDs):
            # Do some query that returns the combined info of a series of adjustments
            closed_adjusted_orders.append(db.session.query(Open, Close).filter(Close.adjustment_id == id).join(Close).all())
            closed_adjusted_trades.append([{**open.opening_trade(), **close.closing_trade()}
                          for open, close in closed_adjusted_orders[idx]])

        # Join Open and Close tables on foreign key open_id
        non_adjusted_orders = db.session.query(Open, Close).filter(Close.adjustment_id == None).join(Close).all()

        # List comprehension to combine open and close dictionaries
        non_adjusted_trades = [{**open.opening_trade(), **close.closing_trade()}
                          for open, close in non_adjusted_orders]

        adjustment_info = []
        for i in closed_adjusted_orders:
            # Gets Ticker and # of adjustments made
            adjustment_info.append((i[0][0].ticker, len(i)))

        return jsonify({
            'success': True,
            'non_adjusted_list': non_adjusted_trades,
            'closed_adjusted_list': closed_adjusted_trades,
            'trades_adjusted': len(closed_adjusted_orders),
            'adjustment_ids': unique_id_list,
            'adjustment_info': adjustment_info
        })

    @app.route('/order-stats', methods=['GET'])
    @requires_auth('get:order-stats')
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
                close_price = db.session.query(
                    Close.close_price, Close.number_contracts).filter(
                    Close.open_id == open_orders[num_opened].id).all()
                ticker_profit = open_orders[num_opened].open_price
                # For every open trade subtract cost of closing trade
                for cost in close_price:
                    # The number of contracts closed serves as a multiplier
                    contracts_closed = close_price[0][1]
                if open_orders[num_opened].buy_sell == 'sell':
                    ticker_profit -= cost[0] * contracts_closed
                else:
                    ticker_profit += cost[0] * contracts_closed
                # Convert decimal to a str for JSON
                totals[open_orders[num_opened].ticker] = str(ticker_profit)
                num_opened += 1

            # Calculate total profit
            for price in totals.values():
                total_profit += float(price)

            return jsonify({
                'success': True,
                'open_orders': len(open_orders),
                'close_orders': len(close_orders),
                'ticker_profit': totals,
                'total_profit': str(round(total_profit, 2))

            })
        except BaseException:
            # Report specific error
            print(sys.exc_info())
            abort(422)

    @app.route('/open-orders', methods=['POST'])
    #@requires_auth('post:open-orders')
    def new_open_order():
        body = request.get_json()
        print(body)
        new_open_date = body.get('openDate', None)
        new_expiration_date = body.get('expirationDate', None)
        new_buy_sell = body.get('buyOrSell', None)
        new_ticker = body.get('ticker', None)
        new_contracts = body.get('numContracts', None)
        new_price = body.get('openPrice', None)
        new_adjustment = body.get('adjustment', None)
        new_adjustment_id = body.get('adjustmentID', None)
        new_closed = body.get('closed', None)
        new_spread = body.get('spread', None)
        new_open_notes = body.get('openNotes', None)
        new_trade_legs = body.get('tradeLegs', None)

        if new_open_date is None:
            abort(400)

        # This is the first adjustment, assign an ID = to original OpenID
        if new_adjustment is True and new_adjustment_id is None:
            # Retrieve OpenID (Only submitted with adjustment forms)
            new_open_id = body.get('openID', None)
            # Establish OpenID as AdjustmentID for tracking
            new_adjustment_id = new_open_id

        try:
            new_trade = Open(
                open_date=new_open_date,
                expiration_date=new_expiration_date,
                buy_or_sell=new_buy_sell,
                ticker=new_ticker,
                number_contracts=new_contracts,
                open_price=new_price,
                spread=new_spread,
                adjustment=new_adjustment,
                adjustment_id=new_adjustment_id,
                closed=new_closed,
                open_notes=new_open_notes,
                trade_legs=new_trade_legs,
            )

            # Add new model to the database
            new_trade.insert()

            #available_orders = Open.query.all()
            #current_trades = [orders.opening_trade()
            #                 for orders in available_orders]

            return jsonify({
                'success': True,
                #'current_trades': current_trades
            })
        except BaseException:
            # Report specific error
            print(sys.exc_info())
            abort(422)

    @app.route('/close-orders', methods=['POST'])
    #@requires_auth('post:close-orders')
    def new_close_order():
        body = request.get_json()
        new_oid = body.get('openID', None)
        new_date = body.get('closeDate', None)
        new_buy_sell = body.get('buyOrSell', None)
        new_contracts = body.get('numContracts', None)
        new_price = body.get('closePrice', None)
        new_adjustment = body.get('adjustment', None)
        new_adjustment_id = body.get('adjustmentID', None)
        new_notes = body.get('closeNotes', None)

        # This is the first adjustment, assign an ID = to original OpenID
        if new_adjustment is True and new_adjustment_id is None:
            # Establish OpenID as AdjustmentID for tracking
            new_adjustment_id = new_oid

        try:
            new_trade = Close(
                open_id=new_oid,
                close_date=new_date,
                buy_sell=new_buy_sell,
                number_contracts=new_contracts,
                close_price=new_price,
                adjustment=new_adjustment,
                adjustment_id=new_adjustment_id,
                close_notes=new_notes,
            )

            new_trade.insert()

            #available_orders = Close.query.all()
            #current_trades = [orders.closing_trade()
            #                  for orders in available_orders]

            return jsonify({
                'success': True,
                #'close_orders': current_trades
            })
        except BaseException:
            # Report specific error
            print(sys.exc_info())
            abort(422)

    @app.route('/open-orders/<int:order_id>', methods=['PATCH'])
    #@requires_auth('patch:open-orders')
    def edit_open_order(order_id):
        selected_order = Open.query.filter(Open.id == order_id).one_or_none()

        # Order not found
        if selected_order is None:
            abort(404)

        body = request.get_json()
        # We have a two types of PATCH operations...one for adjustments and one for edits

        # Edit
        new_open_date = body.get('openDate', None)
        new_expiration_date = body.get('expirationDate', None)
        new_buy_sell = body.get('buyOrSell', None)
        new_ticker = body.get('ticker', None)
        new_contracts = body.get('numContracts', None)
        new_price = body.get('openPrice', None)
        new_spread = body.get('spread', None)
        new_open_notes = body.get('openNotes', None)
        new_trade_legs = body.get('tradeLegs', None)

        # Adjustment
        new_adjustment_id = body.get('adjustmentID', None) # Only used for adjustments to patch original trade adj id
        new_closed = body.get('closed', None) # Used to decide if its an adjust or edit patch. Adjust = True
        
        #new_adjustment = body.get('adjustment', None) -- This param is not currently sent with patch

        # Bad Request
        if new_closed is None:
            abort(400)

        try:
            # New_Closed will always be True for an adjustment patch so use it as the coniditional
            if new_closed:
                # Flag that determines if it's displayed on open trades list
                selected_order.closed = new_closed
                # Ignore empty ID
                if new_adjustment_id is None:
                    pass
                else: 
                    selected_order.adjustment_id = new_adjustment_id
            # Else it's an order edit patch so update all editable fields
            else:
                # Push update to database
                selected_order.open_date = new_open_date
                selected_order.expiration_date = new_expiration_date
                selected_order.buy_or_sell = new_buy_sell
                selected_order.ticker = new_ticker
                selected_order.number_contracts = new_contracts
                selected_order.open_price = new_price
                selected_order.spread = new_spread
                selected_order.open_notes = new_open_notes
                selected_order.trade_legs = new_trade_legs
                     
            selected_order.update()

            return jsonify({
                'success': True,
                'updated_order_id': order_id,
                'new_closed': new_closed
            })

        except BaseException:
            # Report specific error
            print(sys.exc_info())
            abort(422)

    @app.route('/close-orders/<int:order_id>', methods=['PATCH'])
    #@requires_auth('patch:close-orders')
    def edit_close_order(order_id):
        selected_order = Close.query.filter(Close.id == order_id).one_or_none()

        # Order not found
        if selected_order is None:
            abort(404)

        body = request.get_json()
        # Currently only allow updating the description
        new_description = body.get('close_description', None)

        # Bad Request
        if new_description is None:
            abort(400)

        try:
            # Push update to database
            selected_order.close_description = new_description
            selected_order.update()

            return jsonify({
                'success': True,
                'updated_order_id': order_id,
                'new_description': new_description
            })

        except BaseException:
            abort(422)

    @app.route('/open-orders/<int:order_id>', methods=['DELETE'])
    #@requires_auth('delete:open-orders')
    def delete_open_order(order_id):
        # Deleting an open order will delete all matching closing orders
        selected_order = Open.query.filter(Open.id == order_id).one_or_none()

        # Nothing to delete
        if selected_order is None:
            abort(404)

        try:
            selected_order.delete()

            return jsonify({
                'success': True,
                'deleted_id': order_id
            })

        except BaseException:
            # Report specific error
            print(sys.exc_info())
            abort(422)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found!'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable'
        }), 422

    @app.errorhandler(AuthError)
    def authorization_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['code']
        }), error.status_code

    return app


app = create_app()
if __name__ == '__main__':
    app.run()
