from typing import List

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session

Base = declarative_base()


class Tips(Base):
    """
    某些情况下，关于整个游戏的小技巧和知识点提示；
    """
    __tablename__ = 'skill'
    id = Column(Integer, primary_key=True)

    tip = Column(String, comment="提示的具体内容")
