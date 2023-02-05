from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, func,desc

from typing import Optional, List

Base = declarative_base()

engine = create_engine("sqlite:///mydatabase.db")
Session = sessionmaker(bind=engine)
session = Session()


class PlayerLevelExp(Base):
    """
    升级所需经验
    """
    __tablename__ = "player_level_exp"

    id = Column(Integer, primary_key=True)

    level = Column(Integer, comment="等级")
    required_exp = Column(Float, comment="所需经验。非叠加；")


# 增
def add_level_exp(level: int, required_exp: float) -> None:
    """
    新增一条升级所需经验
    :param level: 等级
    :param required_exp: 所需经验
    :return: None
    """
    record = PlayerLevelExp(level=level, required_exp=required_exp)
    session.add(record)
    session.commit()


# 删
def delete_player_level_exp(level_id: int):
    """
    删除某个等级的经验需求

    :param level_id: 要删除的等级的ID
    :return: None
    """
    session.query(PlayerLevelExp).filter(PlayerLevelExp.id == level_id).delete()
    session.commit()


# 改
def update_player_level_exp(level: int, required_exp: float) -> None:
    """
    修改玩家升级所需经验

    Args:
        level: 等级
        required_exp: 所需经验

    Returns:
        None
    """
    player_level_exp = session.query(PlayerLevelExp).filter(PlayerLevelExp.level == level).first()
    player_level_exp.required_exp = required_exp
    session.commit()


# 查
def get_player_level_exp_by_level(level: int) -> PlayerLevelExp:
    """
    根据等级查询对应的经验信息
    :param level: 等级
    :return: 经验信息
    """
    return session.query(PlayerLevelExp).filter(PlayerLevelExp.level == level).first()


def get_max_level():
    """
    获取总经验值
    """
    max_level = session.query(PlayerLevelExp.level).order_by(desc(PlayerLevelExp.level)).first()
    return max_level[0]

def get_total_exp():
    """
    获取总经验值
    """
    total_exp = session.query(func.sum(PlayerLevelExp.required_exp)).scalar()
    return total_exp