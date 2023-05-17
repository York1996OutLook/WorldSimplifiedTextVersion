import cv2
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Optional

from DBHelper.session import session
from DBHelper.tables.base_table import Basic
from DBHelper.tables.base_table import CustomColumn
from Enums import SkillLevel

Base = declarative_base()


class SkillBook(Basic, Base):
    """
    技能卷轴
    """
    __cn__ = "技能卷轴"

    __tablename__ = 'skill_book'
    id = CustomColumn(Integer, cn="ID", primary_key=True, editable=False,autoincrement=True)

    skill_id = CustomColumn(Integer, cn="技能ID", bind_table="Skill", comment="对应的技能ID")
    level = CustomColumn(Integer, cn="等级", bind_type=SkillLevel, comment="技能书的等级,高等级技能书可以学习低等级技能,但是反过来不行")

    cost_health = CustomColumn(Integer, default=0, cn="技能消耗生命值", comment='技能消耗的生命值')
    cost_mana = CustomColumn(Integer, default=0, cn="消耗法力", comment="消耗的法力")
    is_bind = CustomColumn(Boolean, cn="是否绑定", comment="初始是否绑定")

    @classmethod
    def add_or_update_by_id(
            cls,
            *,
            _id: int,

            skill_id: int = None,
            level: int = None,
            days_of_validity: int = None,
            cost_health: int = None,
            cost_mana: int = None,
            is_bind: bool = None
    ):
        record = cls._add_or_update_by_id(kwargs=locals())
        return record

    @classmethod
    def get_by_skill_id_skill_level(cls, *, skill_id: int, level: int):
        record = cls.get_one_by_kwargs(kwargs=locals())
        return record


# 增

# 删

# 改


# 查

def get_skill_book_by_skill_book_id(*,
                                    skill_book_id: int
                                    ) -> SkillBook:
    """
    根据技能书的id查询技能书

    Args:
    skill_book_id: 技能书的id

    Returns:
    List[SkillBook]
    """
    skill_book = session.query(SkillBook).filter_by(skill_book_id=skill_book_id).first()
    return skill_book


def get_by_skill_id_skill_level(*,
                                skill_id: int,
                                level: int
                                ) -> SkillBook:
    """
    查询技能书的记录

    Args:
    skill_id: 技能的id，如果传了这个参数，则只查询指定技能的技能书
    level: 技能书的等级，如果传了这个参数，则只查询指定等级的技能书

    Returns:
    List[SkillBook]
    """
    query = session.query(SkillBook)
    if skill_id is not None:
        query = query.filter_by(skill_id=skill_id)
    if level is not None:
        query = query.filter_by(level=level)

    return query.first()
