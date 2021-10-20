import os

from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'You will never guess...'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:9248jong@localhost:5432/car_collection'
    SQLALCHEMY_TRACK_MODIFICATIONS = False