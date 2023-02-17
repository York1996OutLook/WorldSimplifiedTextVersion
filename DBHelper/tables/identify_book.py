from typing import List

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session

Base = declarative_base()


class IdentifyBook(Base):
    """
    打开 分解 掉落的物品记录
    """
    __tablename__ = 'identify_book'
    id = Column(Integer, primary_key=True)

    name = Column(String, comment="名称")
    is_bind = Column(String, comment="初始获取的时候是否是绑定的")
    introduce = Column(String, comment="介绍")

    def __init__(self, *, name: str, is_bind: bool, introduce: str):
        self.name = name
        self.is_bind = is_bind
        self.introduce = introduce


# 增
def add(*, name: str, is_bind: bool, introduce: str) -> IdentifyBook:
    """
    新增一个book
    :param name:
    :param is_bind:
    :param introduce:
    :return:
    """
    book = IdentifyBook(name=name, is_bind=is_bind, introduce=introduce)
    session.add(book)
    session.commit()
    return book


def add_or_update_by_name(*, identify_book_name: str, is_bind: bool, introduce: str) -> IdentifyBook:
    """
    根据identify_book_name判断是否存在。如果已经存在，则更新，如果不存在，则新建记录；
    :param identify_book_name:
    :param is_bind:
    :param introduce:
    :return:
    """
    if is_exists_by_name(identify_book_name=identify_book_name):
        book = update_by_name(identify_book_name=identify_book_name,
                                            is_bind=is_bind,
                                            introduce=introduce)
    else:
        # 新增
        book = add(name=identify_book_name, is_bind=is_bind, introduce=introduce)
    return book


# 删

# 改
def update_by_name(*, identify_book_name: str, is_bind: bool, introduce: str) -> IdentifyBook:
    """
    更新记录
    :param identify_book_name:
    :param is_bind:
    :param introduce:
    :return:
    """
    book = session.query(IdentifyBook).filter(IdentifyBook.name == identify_book_name).first()
    book.is_bind = is_bind
    book.introduce = introduce
    return book


# 查
def is_exists_by_name(*, identify_book_name: str) -> bool:
    """
    根据名字判断是否存在
    :param identify_book_name:
    :return:
    """
    book = session.query(IdentifyBook).filter(IdentifyBook.name == identify_book_name).first()
    return book is not None


if __name__ == '__main__':
    books = [
        {
            "name": "鉴定卷轴",
            "is_bind": True,
            "introduce": "使用鉴定卷轴，可以使装备获得全新属性。"
        },
        {
            "name": "装备技能鉴定卷轴",
            "is_bind": True,
            "introduce": "使用装备技能鉴定卷轴，可以使某些特殊装备获得全新技能。"
        }
    ]
    for book_dict in books:
        add_or_update_by_name(identify_book_name=book_dict["name"],
                                            is_bind=book_dict['is_bind'],
                                            introduce=['introduce'])
