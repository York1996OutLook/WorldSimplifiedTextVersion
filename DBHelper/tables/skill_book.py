from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Optional

from DBHelper.session import session
from DBHelper.tables.base_table import Basic

Base = declarative_base()


class SkillBook(Basic, Base):
    """
    技能书的列表
    """
    __tablename__ = 'skill_book'

    skill_id = Column(Integer, comment="对应的技能ID")
    level = Column(Integer, comment="技能书的等级,高等级技能书可以学习低等级技能,但是反过来不行")
    days_of_validity = Column(Integer, comment="有效期。以天为单位。如果是-1则代表是永久。参考的技能的ID如果也有有效期,则看具体book的。")

    cost_health = Column(Integer, default=0, comment='技能消耗的生命值')
    cost_mana = Column(Integer, default=0, comment="消耗的法力")
    is_bind = Column(Boolean, comment="初始是否绑定")

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
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
        return record

    @classmethod
    def get_by_skill_id_skill_level(cls, *, skill_id: int, level: int):
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls.get_one_by_kwargs(**fields)
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
