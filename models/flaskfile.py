from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from database_setup import Base
import os
app = Flask(__name__)

APPLICATION_NAME = "Shopping Online"
app.secret_key = os.urandom(24)
# Connect to Database and create database session
engine = create_engine('postgresql://catalog:catalog@localhost/shopwithusers' )
# engine = create_engine('sqlite:///shopwithusers.db')
Base.metadata.bind = engine

DBSession = scoped_session(sessionmaker(bind=engine))
session = DBSession()

