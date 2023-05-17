import os.path as osp

from sqlalchemy import  Integer, String, Boolean,Text
from sqlalchemy.ext.declarative import declarative_base
from typing import List

from DBHelper.session import session
from DBHelper.tables.base_table import Entity
from DBHelper.tables.base_table import CustomColumn
import local_setting
from Utils import tools

Base = declarative_base()


class Box(Entity, Base):
    """
    箱子，一般均可以出售
    """
    __cn__ = "宝箱"

    __tablename__ = 'box'
    id = CustomColumn(Integer, cn="ID", primary_key=True, editable=False,autoincrement=True)
    name = CustomColumn(Text, cn='名称')  # 显式复制并设置 cn 属性

    is_bind = CustomColumn(Boolean,  cn='是否绑定',comment="是否已经绑定")
    introduction = CustomColumn(Text,  cn='介绍',comment="说明")

    @classmethod
    def add_or_update_by_name(cls, *, name: str, is_bind: bool = None, introduction: str = None):
        record = cls._add_or_update_by_name(kwargs=locals())
        return record

    @classmethod
    def add_or_update_by_id(cls, *, _id: int, is_bind: bool = None, introduction: str = None):
        record = cls._add_or_update_by_id(kwargs=locals())
        return record
