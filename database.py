from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os 

if os.environ.get("ENVIRONMENT") == "DEV": 
    engine = create_engine(
        'sqlite:///db.sqlite',
        # echo=True,
        connect_args={'check_same_thread': False}
    )
elif os.environ.get("ENVIRONMENT") == "PROD": 

    DB_USERNAME = os.environ.get("DB_USERNAME")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_HOTE = os.environ.get("DB_HOTE")
    DB_NAME = os.environ.get("DB_NAME")
    DB_PORT = os.environ.get("DB_PORT")

    engine = create_engine(
        f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOTE}:{DB_PORT}/{DB_NAME}",
        connect_args={'check_same_thread': False}
    )
else:
    raise "error to connect to database"


Session = sessionmaker(bind=engine)
session = Session() 


