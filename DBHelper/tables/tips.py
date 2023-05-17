from typing import List

from sqlalchemy import Integer, String, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session
from DBHelper.tables.base_table import Entity
from DBHelper.tables.base_table import CustomColumn

Base = declarative_base()


class Tips(Entity, Base):
    """
    某些情况下,关于整个游戏的小技巧和知识点提示;
    """
    __cn__ = "提示"
    __tablename__ = 'tips'
    id = CustomColumn(Integer, cn="ID", primary_key=True, editable=False,autoincrement=True)

    name = CustomColumn(Text, cn='名称')  # 显式复制并设置 cn 属性

    tip = CustomColumn(Text, cn="提示", comment="提示的具体内容")

    @classmethod
    def add_or_update_by_name(cls,
                              *,
                              name: str = None,
                              tip: str = None
                              ) -> "Tips":
        record = cls._add_or_update_by_name(kwargs=locals())
        return record

    @classmethod
    def add_or_update_by_id(
            cls,
            *,
            _id: int,

            name: str = None,
            tip: str = None
    ) -> "Tips":
        record = cls._add_or_update_by_id(kwargs=locals())
        return record
