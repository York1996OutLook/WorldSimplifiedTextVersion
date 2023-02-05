from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from typing import List

Base = declarative_base()

# 创建数据库连接引擎
engine = create_engine('sqlite:///example.db')

# 创建会话
Session = sessionmaker(bind=engine)
session = Session()


class AchievementRecord(Base):
    """
    将玩家获得的成就记录下来
    """
    __tablename__ = "achievement_record"

    id = Column(Integer, primary_key=True, comment="成就记录ID")

    achievement_id = Column(Integer, comment="成就ID")  # ForeignKey(Achievement.id)
    character_id = Column(Integer, comment="成就达成人物ID")  # ForeignKey(CharacterProperty.id),
    achieve_time = Column(Integer, comment="成就达成时间")


# 增
def insert_achievement_record(achievement_id: int, character_id: int, achieve_time: int) -> None:
    """
    Insert a new record of an achievement

    :param achievement_id: ID of the achievement
    :param character_id: ID of the character who achieved the achievement
    :param achieve_time: Time when the achievement was achieved
    :return: None
    """
    record = AchievementRecord(
        achievement_id=achievement_id,
        character_id=character_id,
        achieve_time=achieve_time
    )
    session.add(record)
    session.commit()


# 删
def delete_achievement_record(record_id: int) -> None:
    """
    Delete an existing record of an achievement

    :param record_id: ID of the record to delete
    :return: None
    """
    record = AchievementRecord.query.get(record_id)
    if record:
        session.delete(record)
        session.commit()



# 改
def update_achievement_record(record_id: int, achievement_id: int = None, character_id: int = None, achieve_time: int = None) -> None:
    """
    Update an existing record of an achievement

    :param record_id: ID of the record to update
    :param achievement_id: (Optional) ID of the achievement
    :param character_id: (Optional) ID of the character who achieved the achievement
    :param achieve_time: (Optional) Time when the achievement was achieved
    :return: None
    """
    record = AchievementRecord.query.get(record_id)
    if record:
        if achievement_id:
            record.achievement_id = achievement_id
        if character_id:
            record.character_id = character_id
        if achieve_time:
            record.achieve_time = achieve_time
        session.commit()

# 查
def get_record_info(record_id: int):
    """
    Retrieve information about a specific achievement record

    :param record_id: ID of the achievement record
    :return: Dictionary with information about the achievement record, None if no record found
    """
    record = AchievementRecord.query.filter_by(id=record_id).first()
    if record:
        return {
            "record_id": record.id,
            "achievement_id": record.achievement_id,
            "character_id": record.character_id,
            "achieve_time": record.achieve_time
        }
    return None

def is_achievement_record_exist(record_id: int) -> bool:
    """
    Check if a record of an achievement exists

    :param record_id: ID of the record to check
    :return: True if the record exists, False otherwise
    """
    return AchievementRecord.query.get(record_id) is not None

# 获取玩家所有成就记录
def get_achievement_records_by_character_id(character_id: int) -> List[AchievementRecord]:
    """
    通过玩家ID获取其所有成就记录
    :param character_id: 玩家ID
    :return: List[AchievementRecord]
    """
    records = session.query(AchievementRecord).filter(AchievementRecord.character_id == character_id).all()
    return records
