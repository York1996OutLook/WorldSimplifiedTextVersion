from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Optional

from DBHelper.session import session
from Enums import ExpBookType

Base = declarative_base()


class ExpBook(Base):
    """
    经验的列表
    """
    __tablename__ = 'exp_book'
    id = Column(Integer, primary_key=True)
    exp_book_type = Column(Integer, comment="经验书的类型，目前只有一种：人物")
    exp_value = Column(Integer, comment="技能书的等级，高等级技能书可以学习低等级技能，但是反过来不行")

    is_bind = Column(Boolean, comment="刚出来的时候是否已经绑定")


if __name__ == '__main__':
    exp_books = [
        ExpBook(base_property_type=ExpBookType.CHARACTER, exp_value=500, is_bind=False),
        ExpBook(base_property_type=ExpBookType.CHARACTER, exp_value=3000, is_bind=False),
        ExpBook(base_property_type=ExpBookType.CHARACTER, exp_value=10000, is_bind=False),
        ExpBook(base_property_type=ExpBookType.CHARACTER, exp_value=20000, is_bind=False),
    ]

    session.add_all(exp_books)
    session.commit()
