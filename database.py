from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(
    'sqlite:///db.sqlite',
    # 'mysql+pymysql://user:password@host:3600/database',
    # db_string = "postgres://admin:donotusethispassword@aws-us-east-1-portal.19.dblayer.com:15813/compose"
    # echo=True,
    connect_args={'check_same_thread': False}
)
Session = sessionmaker(bind=engine)
session = Session() 
