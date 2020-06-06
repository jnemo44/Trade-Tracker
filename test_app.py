import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from database.models import setup_db, Open, Close

# Ensure tests are performed in order
#unittest.TestLoader.sortTestMethodsUsing = None
#unittest.TestLoader.sortTestMethodsUsing = lambda _, x, y: cmp(y, x)


class OrdersTestCase(unittest.TestCase):
    """This class represents the orders test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trade_tracker_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres', 'password', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_open_order = {
            "open_date": "5/26/2020",
            "buy_sell": "sell",
            "ticker": "GPS",
            "number_contracts": 3,
            "open_price": 4.75,
            "adjustment": False,
            "trade_type": "Iron Condor",
            "open_description": "Opening"
        }

        self.new_close_order = {
            "close_date": "6/01/2020",
            "open_id": 1,
            "buy_sell": "buy",
            "number_contracts": 3,
            "close_price": 2.40,
            "adjustment": False,
            "close_description": "Closing"
        }

        self.new_description = {
            "open_description": "This is a new description for testing"
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    # Tests for POST method
    def test01_post_open_order(self):
        "Test a post to open_orders"
        res = self.client().post('/open-orders', json=self.new_open_order)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # def test02_fail_post_open_order(self):
    #    "Test a failed post to open_orders"
    #    res = self.client().post('/open-orders/400')
    #    print(res)
    #    data = json.loads(res.data)

    #    self.assertEqual(res.status_code, 422)
    #    self.assertEqual(data['success'],False)

    def test03_post_close_order(self):
        "Test a post to close_orders"
        res = self.client().post('/close-orders', json=self.new_close_order)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

#    def test04_fail_post_close_order(self):
#        "Test a failed post to close_orders"
#        res = self.client().post('/close-orders/400')
#        data = json.loads(res.data)

#        self.assertEqual(res.status_code, 422)
#        self.assertEqual(data['success'],False)

    # Tests for GET method
    def test05_get_open_orders(self):
        "Test for valid get request"
        res = self.client().get('/open-orders')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test06_get_order_stats(self):
        "Test for invalid get request"
        res = self.client().get('/order-stats')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['ticker_profit'])
        self.assertTrue(data['total_profit'])

    # Add once pagination is implemented
    # def test07_fail_get_order_stats(self):
    #    "Test proper failure of get order-stats request"
    #    res = self.client().get('/order-stats')
    #    data = json.loads(res.data)

    #    self.assertEqual(res.status_code, 404)
    #    self.assertEqual(data['success'],False)

    # Tests for PATCH method

    def test08_edit_order_description(self):
        "Test to successfully edit order description"
        res = self.client().patch(
            '/open-orders/1',
            json={
                'open_description': 'edit'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated_order_id'], 1)

    def test09_fail_edit_description(self):
        "Test that fails to edit the order description"
        res = self.client().patch('/open-orders/4000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # Tests for Delete method
    def test10_delete(self):
        "Test the delete functionality"
        res = self.client().delete('/open-orders/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test11_fail_delete(self):
        "Test that fails to delete"
        res = self.client().delete('/open-orders/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
