from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import  sessionmaker





'''连接数据库的函数'''

HOST = '192.168.31.128'
PORT = '3306'
DATABASE = 'mydb'
USERNAME = 'admin'
PASSWORD = 'Root110qwe'


DB_URL = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
    USERNAME,PASSWORD,HOST,PORT,DATABASE
)

engine = create_engine(DB_URL)
DBSession = sessionmaker(bind=engine)
Base = declarative_base(engine)



