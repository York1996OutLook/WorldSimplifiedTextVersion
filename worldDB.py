from sqlalchemy import create_engine, Column, Integer, String, Enum, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# 全局设置
engine = create_engine('sqlite:///worldSTV.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
