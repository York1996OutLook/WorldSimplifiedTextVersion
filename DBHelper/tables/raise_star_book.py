from typing import List

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session

Base = declarative_base()


class RaiseStarBook(Base):
    """
    打开 分解 掉落的物品记录
    """
    __tablename__ = 'identify_book'
    id = Column(Integer, primary_key=True)

    name = Column(String, comment="名称")
    introduce = Column(String, comment="介绍")

    is_bind = Column(Boolean, comment="新出现的时候是否已经绑定")

    def __init__(self, *, name: str, introduce: str, is_bind: bool):
        self.name = name
        self.introduce = introduce
        self.is_bind = is_bind


# 增

def add(*, name: str, introduce: str, is_bind: bool):
    """

    :param name:
    :param introduce:
    :param is_bind:
    :return:
    """
    book = RaiseStarBook(name=name, introduce=introduce, is_bind=is_bind)
    session.add(book)
    session.commit()
    return book


def add_or_update_by_name(*, name: str, is_bind: bool, introduce: str) -> RaiseStarBook:
    """
    根据raise_star_book_name判断是否存在。如果已经存在，则更新，如果不存在，则新建记录；
    :param name:
    :param is_bind:
    :param introduce:
    :return:
    """
    if is_exists_by_name(name=name):
        book = update_by_name(name=name,
                                              is_bind=is_bind,
                                              introduce=introduce)
    else:
        # 新增
        book = add(name=name, is_bind=is_bind, introduce=introduce)
    return book


# 删

# 改

def update_by_name(*, name: str, is_bind: bool, introduce: str) -> RaiseStarBook:
    """
    更新记录
    :param name:
    :param is_bind:
    :param introduce:
    :return:
    """
    book = session.query(RaiseStarBook).filter(RaiseStarBook.name == name).first()
    book.is_bind = is_bind
    book.introduce = introduce
    return book


# 查
def is_exists_by_name(*, name: str) -> bool:
    """
    根据name判断是否存在
    :param name:
    :return:
    """
    book = session.query(RaiseStarBook).filter(RaiseStarBook.name == name).first()
    return book is not None

def get_by_name(*, name: str) -> RaiseStarBook:
    """
    :param name:
    :return:
    """
    book = session.query(RaiseStarBook).filter(RaiseStarBook.name == name).first()
    return book
