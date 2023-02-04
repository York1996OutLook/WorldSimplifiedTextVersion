

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from typing import List

from worldDB import AchievementRecord

Base = declarative_base()

# 创建数据库连接引擎
engine = create_engine('sqlite:///example.db')

# 创建会话
Session = sessionmaker(bind=engine)
session = Session()


# 获取玩家所有成就记录
def get_achievement_records_by_character_id(character_id: int) -> List[AchievementRecord]:
    """
    通过玩家ID获取其所有成就记录
    :param character_id: 玩家ID
    :return: List[AchievementRecord]
    """
    records = session.query(AchievementRecord).filter(AchievementRecord.character_id == character_id).all()
    return records

# 新增玩家成就记录
def add_achievement_record(achievement_id: int, character_id: int, achieve_time: int) -> None:
    """
    新增玩家成就记录
    :param achievement_id: 成就ID
    :param character_id: 玩家ID
    :param achieve_time: 成就达成时间
    :return: None
    """
    new_record = AchievementRecord(achievement_id=achievement_id, character_id=character_id, achieve_time=achieve_time)
    session.add(new_record)
    session.commit()
