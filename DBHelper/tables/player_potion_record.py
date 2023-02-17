import time
from typing import List

from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session

Base = declarative_base()


class PlayerPotionRecord(Base):
    """
    将玩家使用的药品记录下来。每个用户仅有一个使用药剂记录，使用新的药剂会替换原有药剂；
    """
    __tablename__ = "player_potion_record"

    id = Column(Integer, primary_key=True, comment="药剂类记录ID")

    character_id = Column(Integer, comment="药剂使用者的人物ID")  # ForeignKey(CharacterProperty.id),
    potion_id = Column(Integer, comment="药剂类ID")  # ForeignKey(potion.id)

    take_timestamp = Column(Integer, comment="药剂类最新的使用时间")

    def __init__(self, *, character_id: int, potion_id: int, take_timestamp: int):
        self.character_id = character_id
        self.potion_id = potion_id
        self.take_timestamp = take_timestamp


# 增
def add(*, potion_id: int, character_id: int, take_timestamp: int) -> PlayerPotionRecord:
    """
    Insert a new record of an potion

    :param potion_id: ID of the potion
    :param character_id: ID of the character who achieved the potion
    :param take_timestamp: timestamp when the potion was achieved
    :return: None
    """
    record = PlayerPotionRecord(
        potion_id=potion_id,
        character_id=character_id,
        take_timestamp=take_timestamp
    )
    session.add(record)
    session.commit()
    return record


# 删
def delete_player_potion_record(*, record_id: int) -> None:
    """
    Delete an existing record of an potion

    :param record_id: ID of the record to delete
    :return: None
    """
    record = PlayerPotionRecord.query.get(record_id)
    session.delete(record)
    session.commit()


# 改
def update_by_record_id(*,
                                record_id: int,
                                potion_id: int = None,
                                character_id: int = None,
                                tack_timestamp: int = None) -> None:
    """
    Update an existing record of an potion

    :param record_id: ID of the record to update
    :param potion_id: (Optional) ID of the potion
    :param character_id: (Optional) ID of the character who achieved the potion
    :param tack_timestamp: (Optional) timestamp when the potion was achieved
    :return: None
    """
    record = PlayerPotionRecord.query.get(record_id)
    if potion_id:
        record.potion_id = potion_id
    if character_id:
        record.character_id = character_id
    if tack_timestamp:
        record.tack_timestamp = tack_timestamp
    session.commit()


# 查
def get_by_record_id(*, record_id: int) -> PlayerPotionRecord:
    """
    根据记录id获取player_potion
    """
    record = session.query(PlayerPotionRecord).filter(PlayerPotionRecord.id == record_id)
    return record


def get_by_character_id(*, character_id: int) -> PlayerPotionRecord:
    """
    根据记录id获取player_potion
    """
    record = session.query(PlayerPotionRecord).filter(PlayerPotionRecord.character_id == character_id).first()
    return record


def is_exists(*, record_id: int) -> bool:
    """
    Check if a record of an potion exists

    :param record_id: ID of the record to check
    :return: True if the record exists, False otherwise
    """
    return PlayerPotionRecord.query.get(record_id) is not None

# other
