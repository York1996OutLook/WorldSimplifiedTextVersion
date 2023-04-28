"""
2023年4月23日
"""

from typing import List

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session
from DBHelper.tables.base_table import Basic,Base
from Enums import AchievementType, AdditionalPropertyType


class AchievementTitleBook(Basic,Base):
    """

    """
    __tablename__ = "achievement_title_book"

    achievement_id = Column(Integer, comment="对应的成就ID")
    days_of_validity = Column(Integer, comment="有效期。以天为单位。如果是-1则代表是永久。参考的成就的ID如果也有有效期,则看具体book的。")
    is_bind = Column(Boolean, comment="是否已经绑定")

    @classmethod
    def add_or_update_by_id(
            cls,
            *,
            _id: int,

            achievement_id: int = None,
            days_of_validity: int = None,
            is_bind: bool = None
    ):
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
        return record
