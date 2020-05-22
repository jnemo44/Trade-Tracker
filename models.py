import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

'''
#SQL Lite Database
database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))
'''
# Postgres Database
database_name = "trade_tracker"
database_path = "postgres://{}:{}@{}/{}".format('postgres', 'password','localhost:5432', database_name)

db = SQLAlchemy()

# Setup DB and bind to flask app
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

class Open(db.Model):
    __tablename__ = 'open_orders'

    id = Column(Integer, primary_key=True)
    open_date = Column(DateTime, nullable=False)
    buy_sell = Column(String(5), nullable=False)
    ticker = Column(String(10))
    number_contracts = Column(Integer, nullable=False)
    open_price = Column(Numeric(precision=2), nullable=False)
    adjustment = Column(Boolean, nullable=False)
    trade_type = Column(String(100))
    open_description = Column(String(500))

class Close(db.Model):
    __tablename__ = 'close_orders'

    id = Column(Integer, primary_key=True)
    open_id = Column(Integer, ForeignKey('Open.id'),nullable=False)
    close_date = Column(DateTime, nullable=False)
    buy_sell = Column(String(5), nullable=False)
    number_contracts = Column(Integer, nullable=False)
    close_price = Column(Numeric(precision=2), nullable=False)
    adjustment = Column(Boolean, nullable=False)
    close_description = Column(String(500))
    
    




