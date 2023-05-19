"""
2023年4月23日
"""

from typing import List, Dict, Any

from sqlalchemy import Integer, String, Boolean,Text
from DBHelper.tables.base_table import CustomColumn
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session
from DBHelper.tables.base_table import Entity, Base
from Enums import AdditionalPropertyType


class AchievementTitleBook(Entity, Base):
    """

    """

    __cn__ = "称号书"
    __tablename__ = "achievement_title_book"

    id = CustomColumn(Integer, cn="ID", primary_key=True)
    name = CustomColumn(Text, cn='名称')  # 显式复制并设置 cn 属性

    achievement_id = CustomColumn(Integer, bind_table="Achievement", cn="成就", comment="对应的成就ID")
    days_of_validity = CustomColumn(Integer, cn='有效期', comment="有效期。以天为单位。如果是-1则代表是永久。参考的成就的ID如果也有有效期,则看具体book的。")
    is_bind = CustomColumn(Boolean, cn='是否绑定', comment="是否已经绑定")

    @classmethod
    def add_or_update_by_id(
            cls,
            *,
            _id: int,

            achievement_id: int = None,
            days_of_validity: int = None,
            is_bind: bool = None
    ):
        record = cls._add_or_update_by_id(kwargs=locals())
        return record

    @classmethod
    def add_or_update_by_name(cls,
                              *,
                              name: str,
                              achievement_id: int = None,
                              days_of_validity: int = None,
                              is_bind: bool = None
                              ) -> 'cls':
        record = cls._add_or_update_by_id(kwargs=locals())
