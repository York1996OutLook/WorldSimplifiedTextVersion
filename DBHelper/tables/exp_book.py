import os.path as osp

from sqlalchemy import Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Optional

import local_setting
from DBHelper.session import session
from DBHelper.tables.base_table import Entity
from DBHelper.tables.base_table import CustomColumn

from Enums import ExpBookType
from Utils import tools

Base = declarative_base()


class ExpBook(Entity, Base):
    """
    经验的列表
    """
    __cn__ = "经验书"

    __tablename__ = 'exp_book'
    name = CustomColumn(Integer, cn="名称")

    book_type = CustomColumn(Integer, cn="类型", bind_type=ExpBookType, comment="经验书的类型,目前只有一种:人物")
    exp_value = CustomColumn(Integer, cn="经验值", comment="经验值")

    is_bind = CustomColumn(Boolean, cn="是否绑定", comment="刚出来的时候是否已经绑定")

    @classmethod
    def add_or_update_by_name(cls,
                              *,
                              name: str,

                              book_type: int = None,
                              exp_value: int = None,

                              is_bind: bool = None
                              ) -> "ExpBook":
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_name)
        record = cls._add_or_update_by_name(**fields)
        return record

    # 改
    @classmethod
    def add_or_update_by_id(
            cls,
            *,
            _id: int,

            name: str = None,
            book_type: int = None,
            exp_value: int = None,

            is_bind: bool = None
    ) -> "ExpBook":
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
        return record
