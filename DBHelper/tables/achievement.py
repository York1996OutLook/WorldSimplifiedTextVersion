from typing import List

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session
from Enums import AchievementType, AdditionalPropertyType

Base = declarative_base()


# 成就系统
class Achievement(Base):
    """
    有哪些成就可以达成
    """
    __tablename__ = "achievement"

    id = Column(Integer, primary_key=True, comment="成就ID")
    name = Column(String, comment="成就名称")

    achievement_type = Column(Integer, comment="成就类型")

    condition = Column(String, comment="达成条件")
    introduce = Column(String, comment="对于成就的介绍")

    def __init__(self, *, name: str, achievement_type: AchievementType, condition: str, introduce: str):
        self.name = name
        self.achievement_type = achievement_type
        self.condition = condition
        self.introduce = introduce


# 增
def add(*, name: str, achievement_type: AchievementType, condition: str, introduce: str) -> Achievement:
    """
    创建成就

    Args:
        name (str): 成就名称
        achievement_type (str): 成就名称
        condition (str): 达成条件
        introduce (str): 成就的介绍

    Returns:
        Achievement: 创建的成就
    """
    achievement = Achievement(name=name, achievement_type=achievement_type, condition=condition, introduce=introduce)
    session.add(achievement)
    session.commit()
    return achievement


def add_or_update_achievement(*, name: str, achievement_type: AchievementType, condition: str, introduce: str):
    """

    :param name:
    :param achievement_type:
    :param condition:
    :param introduce:
    :return:
    """
    if is_exists_by_name(name=name):
        return update_by_name(name=name,
                              new_achievement_type=achievement_type,
                              new_condition=condition,
                              new_introduce=introduce,
                              )
    else:
        return add(
            name=name,
            achievement_type=achievement_type,
            condition=condition,
            introduce=introduce,
        )


# 删
def delete_by_achievement_id(*, achievement_id: int) -> bool:
    """
    删除成就

    Args:
        achievement_id (int): 成就id

    Returns:
        bool: 删除是否成功
    """
    achievement = session.query(Achievement).filter_by(id=achievement_id).first()
    session.delete(achievement)
    session.commit()


# 改

def update(*,
           achievement_id: int,
           new_achievement_type: AchievementType = None,
           new_name: str = None,
           new_condition: str = None,
           new_introduce: str = None,
           ) -> Achievement:
    """
    更新成就信息

    Args:
        achievement_id (int): 成就id
        new_achievement_type (int): 成就的类型。
        new_name (str): 新的成就名称
        new_condition (str): 新的达成条件
        new_introduce (str): 新的达成条件

    Returns:
        Achievement: 更新后的成就
    """
    achievement = session.query(Achievement).filter_by(id=achievement_id).first()
    if new_achievement_type:
        achievement.achievement_type = new_achievement_type
    if new_name:
        achievement.name = new_name
    if new_condition:
        achievement.condition = new_condition
    if new_introduce:
        achievement.introduce = new_introduce
    session.commit()
    session.refresh(achievement)
    return achievement


def update_by_name(
        name: str,
        new_achievement_type: AchievementType,
        new_condition: str,
        new_introduce: str, ):
    """

    :param name:
    :param new_achievement_type:
    :param new_condition:
    :param new_introduce:
    :return:
    """
    achievement = session.query(Achievement).filter_by(name=name).first()
    achievement.achievement_type = new_achievement_type
    achievement.condition = new_condition
    achievement.introduce = new_introduce
    session.commit()
    session.refresh(achievement)
    return achievement


# 查
def get_by_achievement_id(*, achievement_id: int) -> Achievement:
    """
    根据id查询成就

    Args:
        achievement_id (int): 成就id

    Returns:
        Achievement: 查询到的成就
    """
    achievement = session.query(Achievement).filter_by(id=achievement_id).first()
    return achievement


def get_by_achievement_name(*, name: str) -> Achievement:
    """
    根据id查询成就

    Args:
        name (str): 成就名字

    Returns:
        Achievement: 查询到的成就
    """
    achievement = session.query(Achievement).filter_by(name=name).first()
    return achievement


def is_exists_by_name(*,
                      name: str
                      ) -> bool:
    """
    根据name查询是否存在；
    :param name:
    :return:
    """
    return session.query(Achievement).filter_by(name=name).scalar() is not None


def get_all() -> List[Achievement]:
    """
    查询所有成就

    Returns:
        List[Achievement]: 所
    有的所有成就列表
    """
    achievements = session.query(Achievement).all()
    return achievements
