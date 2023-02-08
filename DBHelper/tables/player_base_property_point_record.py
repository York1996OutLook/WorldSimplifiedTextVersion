from collections import defaultdict

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Optional, DefaultDict

from Enums import AdditionSourceType,BasePropertyType

Base = declarative_base()
from ..session import session


class PlayerBasePropertyPointRecord(Base):
    """玩家基础体质力量敏捷智力感知的加点的记录表"""
    __tablename__ = 'player_base_property_point_record'

    id = Column(Integer, primary_key=True)

    character_id = Column(Integer, comment="character_id")

    physique_num = Column(Integer, comment='体质')
    strength_num = Column(Integer, comment='力量')
    agility_num = Column(Integer, comment='敏捷')
    intelligence_num = Column(Integer, comment='智力')
    perception_num = Column(Integer, comment='感知')


# 增
def add_player_base_property_point_record(additional_source_type: int, additional_source_id: int, physique_num: int,
                                          strength_num: int, agility_num: int, intelligence_num: int,
                                          perception_num: int) -> PlayerBasePropertyPointRecord:
    """
    添加玩家基础体质力量敏捷智力感知的加点的记录

    Args:
    additional_source_type: 带来属性提升的物品类型，比如成就称号，技能，装备
    additional_source_id: 带来属性提升的物品id
    physique_num: 体质
    strength_num: 力量
    agility_num: 敏捷
    intelligence_num: 智力
    perception_num: 感知

    Returns:
    None if the record is successfully added
    str if an error occurs during the operation
    """
    new_record = PlayerBasePropertyPointRecord(additional_source_type=additional_source_type,
                                               additional_source_id=additional_source_id,
                                               physique_num=physique_num,
                                               strength_num=strength_num,
                                               agility_num=agility_num,
                                               intelligence_num=intelligence_num,
                                               perception_num=perception_num)
    session.add(new_record)
    session.commit()
    return new_record


def get_player_base_property_point_record_by_character_id(character_id: int) -> PlayerBasePropertyPointRecord:
    """
    根据玩家ID查询玩家基础体质力量敏捷智力感知的加点记录

    Args:
    character_id (int): character_id
    Returns:
    player_record (PlayerBasePropertyPointRecord): 玩家基础体质力量敏捷智力感知的加点记录
    """
    player_record = session.query(PlayerBasePropertyPointRecord).filter(
        PlayerBasePropertyPointRecord.character_id == character_id
    ).first()
    return player_record


# other
def get_player_base_property_point_dict_by_character_id(character_id: int) -> DefaultDict[int]:
    """
    将获取到的基础属性转化成字典输出，方便后续读取、修改、累加操作
    :param character_id:
    :return:
    """
    properties_dict = defaultdict(int)

    properties_record = get_player_base_property_point_record_by_character_id(character_id)

    properties_dict[BasePropertyType.PHYSIQUE]=properties_record.physique_num
    properties_dict[BasePropertyType.STRENGTH]=properties_record.strength_num
    properties_dict[BasePropertyType.AGILITY]=properties_record.agility_num
    properties_dict[BasePropertyType.INTELLIGENCE]=properties_record.intelligence_num
    properties_dict[BasePropertyType.PERCEPTION]=properties_record.perception_num

    return properties_dict
