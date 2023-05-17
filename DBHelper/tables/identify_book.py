from typing import List

from sqlalchemy import Integer, String,Text
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session
from DBHelper.tables.base_table import CustomColumn
from DBHelper.tables.base_table import Entity

Base = declarative_base()


class IdentifyBook(Entity, Base):
    __cn__ = "装备属性鉴定卷轴"
    __tablename__ = 'identify_book'
    id = CustomColumn(Integer, cn="ID", primary_key=True, editable=False,autoincrement=True)

    name = CustomColumn(Text, cn='名称')  # 显式复制并设置 cn 属性

    is_bind = CustomColumn(String, cn="是否绑定", comment="初始获取的时候是否是绑定的")
    introduce = CustomColumn(Text, cn="介绍", comment="介绍")

    @classmethod
    def add_or_update_by_name(cls,
                              *,
                              name: str,
                              is_bind: bool = None,
                              introduce: str = None
                              ) -> "IdentifyBook":
        record = cls._add_or_update_by_name(kwargs=locals())
        return record

    @classmethod
    def add_or_update_by_id(
            cls,
            *,
            _id: int,

            name: str = None,
            is_bind: bool = None,
            introduce: str = None
    ) -> "IdentifyBook":
        record = cls._add_or_update_by_id(kwargs=locals())
        return record

#
# if __name__ == '__main__':
#     books = [
#         {
#             "name": "鉴定卷轴",
#             "is_bind": True,
#             "introduce": "使用鉴定卷轴，可以使装备获得全新属性。"
#         },
#         {
#             "name": "装备技能鉴定卷轴",
#             "is_bind": True,
#             "introduce": "使用装备技能鉴定卷轴，可以使某些特殊装备获得全新技能。"
#         }
#     ]
#     for book_dict in books:
#         add_or_update_by_name(identify_book_name=book_dict["name"],
#                               is_bind=book_dict['is_bind'],
#                               introduce=['introduce'])
