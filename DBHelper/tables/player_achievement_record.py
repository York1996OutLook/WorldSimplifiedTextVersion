from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from typing import List

Base = declarative_base()

from DBHelper.session import session



class PlayerAchievementRecord(Base):
    """
    将玩家获得的成就记录下来
    """
    __tablename__ = "player_achievement_record"

    id = Column(Integer, primary_key=True, comment="成就记录ID")

    achievement_id = Column(Integer, comment="成就ID")
    character_id = Column(Integer, comment="成就达成人物ID")
    achieve_timestamp = Column(Integer, comment="成就达成时间")


# 增
def add(*,achievement_id: int, character_id: int, achieve_timestamp: int) -> PlayerAchievementRecord:
    """
    Insert a new record of an achievement

    :param achievement_id: ID of the achievement
    :param character_id: ID of the character who achieved the achievement
    :param achieve_timestamp: timestamp when the achievement was achieved
    :return: None
    """
    record = PlayerAchievementRecord(
        achievement_id=achievement_id,
        character_id=character_id,
        achieve_timestamp=achieve_timestamp
    )
    session.add(record)
    session.commit()
    return record


# 删
def delete(*,record_id: int) -> None:
    """
    Delete an existing record of an achievement

    :param record_id: ID of the record to delete
    :return: None
    """
    record = PlayerAchievementRecord.query.get(record_id)
    session.delete(record)
    session.commit()



# 改
def update(*,
                                     record_id: int,
                                     achievement_id: int = None,
                                     character_id: int = None,
                                     achieve_timestamp: int = None,
                                     ) -> PlayerAchievementRecord:
    """
    Update an existing record of an achievement

    :param record_id: ID of the record to update
    :param achievement_id: (Optional) ID of the achievement
    :param character_id: (Optional) ID of the character who achieved the achievement
    :param achieve_timestamp: (Optional) timestamp when the achievement was achieved
    :return: None
    """
    record = PlayerAchievementRecord.query.get(record_id)
    if achievement_id:
        record.achievement_id = achievement_id
    if character_id:
        record.character_id = character_id
    if achieve_timestamp:
        record.achieve_timestamp = achieve_timestamp
    session.commit()
    session.refresh(record)
    return record

# 查
def get_by_record_id(*,record_id: int):
    """
    Retrieve information about a specific achievement record

    :param record_id: ID of the achievement record
    :return: Dictionary with information about the achievement record, None if no record found
    """
    record = PlayerAchievementRecord.query.filter_by(id=record_id).first()
    return record

def is_exists_by_record_id(*,record_id: int) -> bool:
    """
    Check if a record of an achievement exists

    :param record_id: ID of the record to check
    :return: True if the record exists, False otherwise
    """
    return PlayerAchievementRecord.query.get(record_id) is not None

# 获取玩家所有成就记录
def get_all_by_character_id(*,character_id: int) -> List[PlayerAchievementRecord]:
    """
    通过玩家ID获取其所有成就记录
    :param character_id: 玩家ID
    :return: List[AchievementRecord]
    """
    records = session.query(PlayerAchievementRecord).filter(PlayerAchievementRecord.character_id == character_id).all()
    return records

def get_title_by_character_id(*,character_id: int) -> PlayerAchievementRecord:
    """
    通过玩家ID获取其所有成就记录
    :param character_id: 玩家ID
    :return: List[AchievementRecord]
    """
    record = session.query(PlayerAchievementRecord).filter(PlayerAchievementRecord.character_id == character_id).first()
    return record

# other



