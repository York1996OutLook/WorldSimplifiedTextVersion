from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from typing import List

Base = declarative_base()

# 创建数据库连接引擎
engine = create_engine('sqlite:///example.db')

# 创建会话
Session = sessionmaker(bind=engine)
session = Session()


class SkillBook(Base):
    """
    技能书的列表
    """
    __tablename__ = 'skill_book'
    id = Column(Integer, primary_key=True)
    skill_id = Column(Integer, comment="参考技能表")
    level = Column(Integer, comment="技能书的等级，高等级技能书可以学习低等级技能，但是反过来不行")

