from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from typing import List

from DBHelper.session import session

Base = declarative_base()


class Box(Base):
    """
    箱子，一般均可以出售
    """
    __tablename__ = 'Box'

    id = Column(Integer, primary_key=True)
    name = Column(String, comment="物品的中文名字")

    introduction = Column(String, comment="说明")

    is_bind = Column(Boolean, comment="是否已经绑定")