import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Config:
    APIKEY=os.environ.get("APIKEY","not set")
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL','db.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS",False)
    SQLALCHEMY_ECHO = os.environ.get("SQLALCHEMY_ECHO",False)
    SAVEDIR = os.environ.get("SAVEDIR","")
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "DEBUG")
    APININJASKEY = os.environ.get("APININJASKEY","not set")
