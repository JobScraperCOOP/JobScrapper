from sqlalchemy import create_engine, Column, String,Integer,FLOAT
from sqlalchemy.ext.declarative import declarative_base
import db
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Job(Base):
    __tablename__ = "jobs"

    index = Column('index', Integer, index=True, primary_key=True)
    title = Column('title', String)
    jobCategory = Column('category', String)
    code = Column('code', String, unique=True, nullable=False)
    link = Column('link', String)
    region = Column('region', String)
    city = Column('city', String)
    lastUpdated = Column('last_update',FLOAT)

    def __init__(self, title, jobCategory, code, link, region, city, lastUpdated):
        self.title = title
        self.jobCategory = jobCategory
        self.code = code
        self.link = link
        self.region = region
        self.city = city
        self.lastUpdated = lastUpdated


engine = create_engine('sqlite:///jobs.db', echo=False)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()




# CREATE TABLE `heroku_f01bf6ee851e78d`.`new_table` (
#   `index` INT NOT NULL AUTO_INCREMENT,
#   `title` VARCHAR(45) NULL,
#   `category` VARCHAR(45) NULL,
#   `code` VARCHAR(45) NOT NULL,
#   `link` VARCHAR(45) NULL,
#   `region` VARCHAR(45) NULL,
#   `city` VARCHAR(45) NULL,
#   `last_update` FLOAT NULL,
#   PRIMARY KEY (`index`),
#   UNIQUE INDEX `code_UNIQUE` (`code` ASC))
# ENGINE = InnoDB
# DEFAULT CHARACTER SET = utf8
# COLLATE = utf8_unicode_ci;
