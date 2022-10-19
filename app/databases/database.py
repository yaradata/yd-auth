import os, sys
from dotenv import load_dotenv

from tortoise.contrib.fastapi import register_tortoise

load_dotenv()

folder = os.path.dirname(os.path.abspath('../'))
sys.path.insert(0, folder)

if os.environ.get("ENVIRONMENT") == "DEV": 
    DB_URL = 'sqlite://databases/db.sqlite3'

elif os.environ.get("ENVIRONMENT") == "PROD": 
    DB_USERNAME = os.environ.get("DB_USERNAME")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_HOTE = os.environ.get("DB_HOTE")
    DB_NAME = os.environ.get("DB_NAME")
    DB_PORT = os.environ.get("DB_PORT")
    
    DB_URL = 'postgres://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOTE + ':' + DB_PORT + '/' + DB_NAME
    

else:
    raise "error while connecting to database"


def init_database(app): 
    register_tortoise(
        app,
        db_url = DB_URL,
        modules = { 'models': ['models.User'] },
        generate_schemas = True,
        add_exception_handlers = True
    )