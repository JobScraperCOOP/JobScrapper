from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Job(Base):
    __tablename__ = "jobs"


    index = Column('index', Integer, index=True, primary_key=True)
    title = Column('title', String)
    jobCategory = Column('category', String)
    code = Column('code', String)
    link = Column('link', String)
    region = Column('region', String)
    city = Column('city', String)

    def __init__(self,title, jobCategory, code, link, region, city):
        self.title = title
        self.jobCategory = jobCategory
        self.code = code
        self.link = link
        self.region = region
        self.city = city