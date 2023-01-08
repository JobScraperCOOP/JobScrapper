from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
dbname = 'heroku_f01bf6ee851e78d'
host = 'eu-cdbr-west-03.cleardb.net'
password = 'bddba042'
username = 'b1b0594abe7e68'
port = ''
url = 'mysql://'+username+':'+password+'@'+host+'/'+dbname

print(url)
engine = create_engine('sqlite:///jobs.db', echo=False)
# engine = create_engine(url, echo=False)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
