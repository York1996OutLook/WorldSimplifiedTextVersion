


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


from worldDB import Achievement

Base = declarative_base()

# 创建数据库连接引擎
engine = create_engine('sqlite:///example.db')

# 创建会话
Session = sessionmaker(bind=engine)
session = Session()

def create_achievement(name: str, condition: str) -> Achievement:
    """
    创建成就

    Args:
        name (str): 成就名称
        condition (str): 达成条件

    Returns:
        Achievement: 创建的成就
    """
    achievement = Achievement(name=name, condition=condition)
    session.add(achievement)
    session.commit()
    return achievement


def get_achievement_by_id(achievement_id: int) -> Achievement:
    """
    根据id查询成就

    Args:
        achievement_id (int): 成就id

    Returns:
        Achievement: 查询到的成就
    """
    achievement = session.query(Achievement).filter_by(id=achievement_id).first()
    return achievement


def update_achievement(achievement_id: int, new_name: str, new_condition: str) -> Achievement:
    """
    更新成就信息

    Args:
        achievement_id (int): 成就id
        new_name (str): 新的成就名称
        new_condition (str): 新的达成条件

    Returns:
        Achievement: 更新后的成就
    """
    achievement = session.query(Achievement).filter_by(id=achievement_id).first()
    if achievement:
        achievement.name = new_name
        achievement.condition = new_condition
        session.commit()
    return achievement


def delete_achievement(achievement_id: int) -> bool:
    """
    删除成就

    Args:
        achievement_id (int): 成就id

    Returns:
        bool: 删除是否成功
    """
    achievement = session.query(Achievement).filter_by(id=achievement_id).first()
    if achievement:
        session.delete(achievement)
        session.commit()
        return True
    else:
        return False


def get_all_achievements() -> List[Achievement]:
    """
    查询所有成就

    Returns:
        List[Achievement]: 所
    有的所有成就列表
    """
    achievements = session.query(Achievement).all()
    return achievements