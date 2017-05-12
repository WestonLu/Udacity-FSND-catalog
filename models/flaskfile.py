from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base

app = Flask(__name__)

APPLICATION_NAME = "Shopping Online"

# Connect to Database and create database session
engine = create_engine('sqlite:///shopwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()