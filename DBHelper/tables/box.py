import os.path as osp

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from typing import List

from DBHelper.session import session
from DBHelper.tables.base_table import Entity
import local_setting
from Utils import tools

Base = declarative_base()


class Box(Entity):
    """
    箱子，一般均可以出售
    """

    __tablename__ = 'box'

    is_bind = Column(Boolean, comment="是否已经绑定")

    introduction = Column(String, comment="说明")

    @classmethod
    def add_or_update_by_name(cls, *, name: str, is_bind: bool=None, introduction: str=None):
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_name(**fields)
        return record


    @classmethod
    def add_or_update_by_id(cls, *, _id: int, is_bind: bool=None, introduction: str=None):
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
        return record
