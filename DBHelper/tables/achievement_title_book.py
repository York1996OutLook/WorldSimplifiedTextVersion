"""
2023年4月23日
"""

from typing import List

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session
from Enums import AchievementType, AdditionalPropertyType

Base = declarative_base()


# 成就系统
class AchievementTitleBook(Base):
    """

    """
    __tablename__ = "achievement_title_book"

    id = Column(Integer, primary_key=True, comment="成就ID")

    achievement_id = Column(Integer, comment="对应的成就ID")
    days_of_validity = Column(Integer, comment="有效期。以天为单位。如果是-1则代表是永久。参考的成就的ID如果也有有效期，则看具体book的。")
    is_bind = Column(Boolean, comment="是否已经绑定")

    def __init__(self,
                 *,
                 achievement_id: int,
                 days_of_validity: int,
                 is_bind: bool,
                 ):
        self.achievement_id = achievement_id

        self.days_of_validity = days_of_validity
        self.is_bind = is_bind
