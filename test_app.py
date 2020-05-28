import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from database.models import setup_db, Open, Close

class OpenOrdersTestCase(unittest.TestCase):
    """This class represents the orders test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trade_tracker_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'password','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_order = {
            "open_date":"5/26/2020",
            "buy_sell":"sell",
            "ticker":"GPS",
            "number_contracts":3,
            "open_price":4.75,
            "adjustment":False,
            "trade_type":"Iron Condor",
            "open_description":"Keep it wide kid"
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

    #Tests for GET method
    def test_get_open_orders(self):
        "Test for valid get request"
        res = self.client().get('/open-orders')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
