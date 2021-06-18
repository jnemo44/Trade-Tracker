import os
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Numeric,
    Boolean,
    String,
    ForeignKey
)
from sqlalchemy.sql.sqltypes import BOOLEAN

'''
#SQL Lite Database
database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))
'''
# Postgres Database
database_name = "trade_tracker"
# Local Dev
database_path = "postgres://{}:{}@{}/{}".format(
    'jniemiec', 'password', 'localhost:5432', database_name)
# database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()


# Setup DB and bind to flask app
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # Not needed if using migrations
    # db.create_all()


# Use to re-initialize a clean database
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

# Extend the base model class to add common methods


class HelperFunctions(db.Model):
    __abstract__ = True

    # Adds new entry to the database
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # Update exsisting order
    def update(self):
        db.session.commit()

    # Delete open order
    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Open(HelperFunctions):
    __tablename__ = 'open_orders'

    id = Column(Integer, primary_key=True)
    open_date = Column(DateTime, nullable=False)
    expiration_date = Column(DateTime, nullable=False)
    buy_or_sell = Column(String(5), nullable=False)
    ticker = Column(String(10), nullable=False)
    number_contracts = Column(Integer, nullable=False)
    open_price = Column(Numeric(precision=10, scale=2), nullable=False)
    adjustment = Column(Boolean, nullable=False)
    closed = Column(Boolean, nullable=False)
    spread = Column(String(100))
    open_notes = Column(String(500))
    # Relationship is one to many (An open order can have multiple close
    # orders)
    open_close = db.relationship(
        'Close',
        backref='open',
        cascade='all,delete',
        passive_deletes=True,
        lazy=True,
    )

    def opening_trade(self):
        return {
            'id': self.id,
            'openDate': self.open_date,
            'expirationDate': self.expiration_date,
            'buyOrSell': self.buy_or_sell,
            'ticker': self.ticker,
            'numContracts': self.number_contracts,
            'openPrice': str(self.open_price),
            'adjustment': self.adjustment,
            'spread': self.spread,
            'openNotes': self.open_notes
        }


class Close(HelperFunctions):
    __tablename__ = 'close_orders'

    id = Column(Integer, primary_key=True)
    # Add foreign key on delete of open_order 
    # delete all coresponding closing orders
    open_id = Column(
        Integer,
        ForeignKey(
            'open_orders.id',
            ondelete='cascade'),
        nullable=False)
    close_date = Column(DateTime, nullable=False)
    buy_sell = Column(String(5), nullable=False)
    number_contracts = Column(Integer, nullable=False)
    close_price = Column(Numeric(precision=10, scale=2), nullable=False)
    adjustment = Column(Boolean, nullable=False)
    close_notes = Column(String(400))

    def closing_trade(self):
        return {
            'closeID': self.id,
            'openID': self.open_id,
            'closeDate': self.close_date,
            'buyOrSell': self.buy_sell,
            'numContracts': self.number_contracts,
            'closePrice': str(self.close_price),
            'adjustment': self.adjustment,
            'closeNotes': self.close_notes
        }
