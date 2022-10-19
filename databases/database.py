import os, sys

from tortoise.contrib.fastapi import register_tortoise

folder = os.path.dirname(os.path.abspath('../'))
sys.path.insert(0, folder)

from main import app

if os.environ.get("ENVIRONMENT") == "DEV": 
    DB_URL = 'sqlite://databases/db.sqlite3'

elif os.environ.get("ENVIRONMENT") == "PROD": 
    # DB_URL = 
    DB_USERNAME = os.environ.get("DB_USERNAME")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_HOTE = os.environ.get("DB_HOTE")
    DB_NAME = os.environ.get("DB_NAME")
    DB_PORT = os.environ.get("DB_PORT")

else:
    raise "error to connect to database"

register_tortoise(
    app,
    db_url = DB_URL,
    modules = { 'models': ['models.User'] },
    generate_schemas = True,
    add_exception_handlers = True
)