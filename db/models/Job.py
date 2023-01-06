from sqlalchemy import create_engine, Column, String,Integer,FLOAT
from sqlalchemy.ext.declarative import declarative_base
import db
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Job(Base):
    __tablename__ = "jobs"

    index = Column('index', Integer, index=True, primary_key=True)
    title = Column('title', String)
    job_category = Column('category', String)
    code = Column('code', String, unique=True, nullable=False)
    link = Column('link', String)
    region = Column('region', String)
    city = Column('city', String)
    lastUpdated = Column('last_update',FLOAT)

    def __init__(self, title, job_category, code, link, region, city, lastUpdated):
        self.title = title
        self.job_category = job_category
        self.code = code
        self.link = link
        self.region = region
        self.city = city
        self.lastUpdated = lastUpdated


engine = create_engine('sqlite:///jobs.db', echo=False)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
