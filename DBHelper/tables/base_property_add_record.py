from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, Enum, Float, Boolean

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from DBHelper.session import session


class BasePropertyAddRecord(Base):
    """
    基础属性名称: 体质、力量、敏捷、感知、智力
    """

    __tablename__ = 'base_property_add_record'
    id = Column(Integer, primary_key=True)

    character_id = Column(Integer, comment="character_id")
    physique_num = Column(Integer, comment="体质")
    strength_num = Column(Integer, comment="力量")
    agility_num = Column(Integer, comment="敏捷")
    intelligence_num = Column(Integer, comment="智力")
    perception_num = Column(Integer, comment="感知")

    last_update_timestamp = Column(Integer, comment="修改或者新增的时间")


# 增
def add_base_property_add_record(character_id: int,
                                 physique_num: int,
                                 strength_num: int,
                                 agility_num: int,
                                 intelligence_num: int,
                                 perception_num: int,
                                 last_update_timestamp: int,
                                 ) -> BasePropertyAddRecord:
    """
    Add a new record to the BasePropertyAddRecord table.

    :param character_id: the player id (int)
    :param physique_num: the value of the physique property (int)
    :param strength_num: the value of the strength property (int)
    :param agility_num: the value of the agility property (int)
    :param intelligence_num: the value of the intelligence property (int)
    :param perception_num: the value of the perception property (int)
    :param last_update_timestamp: update or add timestamp
    :return: None
    """

    # Create a new record
    new_record = BasePropertyAddRecord(
        character_id=character_id,

        physique_num=physique_num,
        strength_num=strength_num,
        agility_num=agility_num,
        intelligence_num=intelligence_num,
        perception_num=perception_num,

        last_update_timestamp=last_update_timestamp
    )

    # Add the new record to the session
    session.add(new_record)

    # Commit the changes to the database
    session.commit()
    return new_record


# 删
def delete_base_property_add_record(record_id: int):
    """
    Delete a base property add record by its ID.
    """
    # Get the record to delete
    record = session.query(BasePropertyAddRecord).filter_by(id=record_id).first()

    # If the record exists, delete it
    if record:
        session.delete(record)
        session.commit()
    else:
        raise Exception("Record with id {} not found.".format(record_id))


# 改
def update_base_property_add_record(record_id, character_id=None, physique_num=None, strength_num=None,
                                    agility_num=None, intelligence_num=None, perception_num=None,
                                    last_update_timestamp=None):
    """
    Update a BasePropertyAddRecord record.

    :param record_id: ID of the record to update
    :param character_id: Updated player ID (optional)
    :param physique_num: Updated physique number (optional)
    :param strength_num: Updated strength number (optional)
    :param agility_num: Updated agility number (optional)
    :param intelligence_num: Updated intelligence number (optional)
    :param perception_num: Updated perception number (optional)
    :param last_update_timestamp: Updated timestamp (optional)
    """
    record = session.query(BasePropertyAddRecord).filter(BasePropertyAddRecord.id == record_id).first()

    if record:
        if character_id is not None:
            record.character_id = character_id
        if physique_num is not None:
            record.physique_num = physique_num
        if strength_num is not None:
            record.strength_num = strength_num
        if agility_num is not None:
            record.agility_num = agility_num
        if intelligence_num is not None:
            record.intelligence_num = intelligence_num
        if perception_num is not None:
            record.perception_num = perception_num
        if last_update_timestamp is not None:
            record.timestamp = last_update_timestamp

        session.commit()
    else:
        raise Exception("Record with id {} not found.".format(record_id))


# 查
def query_base_property_add_record_by_id(record_id: int):
    """
    根据id查询BasePropertyAddRecord记录
    :param record_id: 记录的id
    :return: 记录对象，如果不存在，返回None
    """
    record = session.query(BasePropertyAddRecord).filter_by(id=record_id).first()
    return record


def query_base_property_add_record_by_character_id(character_id: int) -> List[BasePropertyAddRecord]:
    """
    查询某个角色的基础属性加成记录

    :param character_id: 角色 id
    :return: 该的基础属性加成记录列表
    """
    return session.query(BasePropertyAddRecord).filter(BasePropertyAddRecord.character_id == character_id).all()


def record_exists(character_id: int) -> bool:
    # Create a SQLAlchemy engine
    record = session.query(BasePropertyAddRecord).filter_by(character_id=character_id).first()
    # Return True if the record exists, False otherwise
    return record is not None
