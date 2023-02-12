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


if __name__ == '__main__':
    books = [
        RaiseStarBook(name="升星卷轴",
                      introduce="",
                      is_bind=True,
                      ),
    ]
    session.add_all(books)
    session.commit()
