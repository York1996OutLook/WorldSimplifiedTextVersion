from typing import List

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session
from Enums import AchievementType, AdditionalPropertyType

Base = declarative_base()


"""
如果是第一次进入游戏，达成条件对应的属性为空。属性值为空。
如果是基础属性突破，则属性和值均可填写。
如果是等级相关，则对应属性为空，属性值为等级；
如果是击杀boss相关，则对应属性为空，属性值为击杀数量。击杀数量通过击杀表来体现；
如果是FIRST_PK，则对应属性为空，属性值为空；
如果是PK_RANK，则对应属性为空，属性值为排名；
如果是GOLD_NUM_INCREASE，则对应属性为空，属性值为黄金数量；
如果是FIRST_SKILL，则对应属性类型为空，属性值为空。
如果是SKILL，则对应属性类型为空，属性值为技能数；
如果是FULL_SKILL，则对应属性类型为空，属性值为满9的个数；
如果是FIRST_LOTTERY,则对应属性类型为空，属性值为空。初次抽奖触发
如果是LOTTERY，则对应属性类型为空，属性值为中奖次数
如果是FULL_EQUIPMENT，则对应属性类型为空，属性值为穿戴装备数量；
如果是EQUIPMENT，则对应属性类型为品质id，属性值为数量。含义为，穿戴装备均在某个品质及以上；
如果是FIRST_SELL_STUFF，则对应属性为空，属性值为空。
如果是FIRST_EXP_BOOK,则对应属性为类型为空，属性值为空。
如果是FIRST_IDENTIFY,则对应属性为类型空，属性值为空。
如果是FIRST_RAISE_STAR，则对应属性类型为空，属性值为空。
如果是RAISE_STAR，则对应属性类型为空，属性值为所穿戴装备中最高的升星数量。
如果是ALL_RAISE_STAR，则对应属性类型为空，属性值为所有穿戴装备升星数量。
"""

# 成就系统
class Achievement(Base):
    """
    有哪些成就可以达成
    """
    __tablename__ = "achievement"

    id = Column(Integer, primary_key=True, comment="成就ID")
    name = Column(String, comment="成就名称")

    achievement_type = Column(Integer, comment="成就类型")

    condition_property_type = Column(Integer, comment="达成条件对应的属性")
    condition_property_value = Column(Integer, comment="达成条件对应属性应该达到的值。")
    achievement_point = Column(Integer, comment="根据达成难度获得成就点数")
    days_of_validity = Column(Integer, comment="有效期。以天为单位")
    introduce = Column(String, comment="对于成就的介绍")

    def __init__(self,
                 *,
                 name: str,
                 achievement_type: AchievementType,
                 condition_type: int,
                 achievement_point: int,
                 days_of_validity: int,
                 introduce: str, ):
        self.name = name
        self.achievement_type = achievement_type
        self.condition_type = condition_type
        self.achievement_point = achievement_point
        self.days_of_validity = days_of_validity
        self.introduce = introduce


# 增
def add(*,
        name: str,
        achievement_type: AchievementType,
        condition_type: int,
        achievement_point: int,
        days_of_validity: int,
        introduce: str, ) -> Achievement:
    """
    创建成就

    Args:
        name (str): 成就名称
        achievement_type (str): 成就名称
        condition_type (str): 达成条件
        achievement_point (str): 成就点数
        days_of_validity (str): 有效期，以天为单位
        introduce (str): 成就的介绍

    Returns:
        Achievement: 创建的成就
    """
    achievement = Achievement(name=name,
                              achievement_type=achievement_type,
                              condition_type=condition_type,
                              achievement_point=achievement_point,
                              days_of_validity=days_of_validity,
                              introduce=introduce)
    session.add(achievement)
    session.commit()
    return achievement


def add_or_update_achievement(*, name: str, achievement_type: AchievementType, condition_type: str, introduce: str):
    """

    :param name:
    :param achievement_type:
    :param condition_type:
    :param introduce:
    :return:
    """
    if is_exists_by_name(name=name):
        return update_by_name(name=name,
                              new_achievement_type=achievement_type,
                              new_condition_type=condition_type,
                              new_introduce=introduce,
                              )
    else:
        return add(
            name=name,
            achievement_type=achievement_type,
            condition_type=condition_type,
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
           new_condition_type: str = None,
           new_introduce: str = None,
           ) -> Achievement:
    """
    更新成就信息

    Args:
        achievement_id (int): 成就id
        new_achievement_type (int): 成就的类型。
        new_name (str): 新的成就名称
        new_condition_type (str): 新的达成条件
        new_introduce (str): 新的达成条件

    Returns:
        Achievement: 更新后的成就
    """
    achievement = session.query(Achievement).filter_by(id=achievement_id).first()
    if new_achievement_type:
        achievement.achievement_type = new_achievement_type
    if new_name:
        achievement.name = new_name
    if new_condition_type:
        achievement.condition_type = new_condition_type
    if new_introduce:
        achievement.introduce = new_introduce
    session.commit()
    session.refresh(achievement)
    return achievement


def update_by_name(
        name: str,
        new_achievement_type: AchievementType,
        new_condition_type: str,
        new_introduce: str, ):
    """

    :param name:
    :param new_achievement_type:
    :param new_condition_type:
    :param new_introduce:
    :return:
    """
    achievement = session.query(Achievement).filter_by(name=name).first()
    achievement.achievement_type = new_achievement_type
    achievement.condition_type = new_condition_type
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
