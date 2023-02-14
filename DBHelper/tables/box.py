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
    name = Column(String, comment="箱子的中文名字")

    introduction = Column(String, comment="说明")
    is_bind = Column(Boolean, comment="是否已经绑定")



if __name__ == '__main__':
    boxes = [
        Box(name=ExpBookType.CHARACTER, introduction=500, is_bind=False),
        Box(name=ExpBookType.CHARACTER, introduction=3000, is_bind=False),
        Box(name=ExpBookType.CHARACTER, introduction=10000, is_bind=False),
        Box(name=ExpBookType.CHARACTER, introduction=20000, is_bind=False),
    ]

    session.add_all(exp_books)
    session.commit()
