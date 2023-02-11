from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///F:\Python-code\WorldSimplifiedTextVersion\DBHelper\worldSTV.db')

Session = sessionmaker(bind=engine)
session = Session()
