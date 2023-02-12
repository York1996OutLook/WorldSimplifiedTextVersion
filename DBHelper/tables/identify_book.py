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
    introduce = Column(String, comment="介绍")


if __name__ == '__main__':
    books = [
        IdentifyBook(name="鉴定卷轴",
                     introduce="对装备使用鉴定卷轴，可以获得全新属性。",
                     ),
    ]
    session.add_all(books)
    session.commit()
