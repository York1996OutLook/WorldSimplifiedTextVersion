from typing import List

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session
from DBHelper.tables.base_table import Entity

Base = declarative_base()

class IdentifyBook(Entity):
    """
    打开 分解 掉落的物品记录
    """
    __tablename__ = 'identify_book'
    is_bind = Column(String, comment="初始获取的时候是否是绑定的")
    introduce = Column(String, comment="介绍")

    @classmethod
    def add_or_update_by_name(cls,
                              *,
                              name: str,
                              is_bind: bool = None,
                              introduce: str = None
                              ) -> "IdentifyBook":
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_name)
        record = cls._add_or_update_by_name(**fields)
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
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
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
