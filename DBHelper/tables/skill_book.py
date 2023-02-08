from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Optional

Base = declarative_base()

from ..session import session


class SkillBook(Base):
    """
    技能书的列表
    """
    __tablename__ = 'skill_book'
    id = Column(Integer, primary_key=True)
    skill_id = Column(Integer, comment="参考技能表")
    level = Column(Integer, comment="技能书的等级，高等级技能书可以学习低等级技能，但是反过来不行")


# 增

# 删

# 改


# 查

def get_skill_book_by_skill_book_id(skill_book_id:int)->SkillBook:
    """
    根据技能书的id查询技能书

    Args:
    skill_book_id: 技能书的id

    Returns:
    List[SkillBook]
    """
    skill_book = session.query(SkillBook).filter_by(skill_book_id=skill_book_id).first()
    return skill_book

def get_skill_id_by_skill_book_id(skill_book_id: int) -> SkillBook:
    """
    查询技能书的记录

    Args:
    skill_id: 技能的id，如果传了这个参数，则只查询指定技能的技能书
    level: 技能书的等级，如果传了这个参数，则只查询指定等级的技能书

    Returns:
    List[SkillBook]
    """
    query = session.query(SkillBook).filter_by(skill_book_id=skill_book_id)
    return query.first()


def get_skill_book_by_skill_id_skill_level(skill_id: int, level: int) -> SkillBook:
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
