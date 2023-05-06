import os.path as osp

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Optional

import local_setting
from DBHelper.session import session
from DBHelper.tables.base_table import Entity
from Enums import ExpBookType
from Utils import tools

Base = declarative_base()

class ExpBook(Entity,Base):
    """
    经验的列表
    """
    __tablename__ = 'exp_book'
    id = Column(Integer, primary_key=True)
    name = Column(String, comment="经验书的名字")
    book_type = Column(Integer, comment="经验书的类型,目前只有一种:人物")
    exp_value = Column(Integer, comment="技能书的等级,高等级技能书可以学习低等级技能,但是反过来不行")

    is_bind = Column(Boolean, comment="刚出来的时候是否已经绑定")

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


