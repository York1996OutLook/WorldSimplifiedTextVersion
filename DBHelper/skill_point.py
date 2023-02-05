from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Optional

Base = declarative_base()

# 创建数据库连接引擎
engine = create_engine('sqlite:///example.db')

# 创建会话
Session = sessionmaker(bind=engine)
session = Session()




class SkillPoint(Base):
    """
    升级技能需要的技能点
    """
    __tablename__ = 'skill_point'
    id = Column(Integer, primary_key=True)
    level = Column(Integer, comment="等级")
    need_point = Column(Integer, comment="所需技能点")
