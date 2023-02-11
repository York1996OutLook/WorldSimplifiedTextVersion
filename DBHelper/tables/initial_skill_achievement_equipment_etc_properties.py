
from collections import defaultdict
from typing import Optional,DefaultDict,List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String,Boolean
from sqlalchemy.ext.declarative import declarative_base



from Enums import AdditionSourceType,AdditionalPropertyType

Base = declarative_base()
from DBHelper.session import session


class InitialSkillAchievementEquipmentEtcPropertiesRecord(Base):
    """初始属性，基础属性加点、技能、装备、称号等常见的所有属性表，为永久表"""
    __tablename__ = 'initial_skill_achievement_equipment_etc_properties_record'

    id = Column(Integer, primary_key=True)

    additional_source_type = Column(Integer, comment="带来属性提升的物品类型，比如成就初始属性，基础属性加点，称号，技能，装备")

    additional_source_id = Column(Integer, comment="""
带来属性提升的物品id。
如果是初始属性，则此项为character id。
如果基础属性，则此项为character id。
如果是称号，则此项为character_id。
如果是技能，则此项为skill_book_id。
如果是装备，则此项为stuff_record_id。
    """)

    additional_source_property_index = Column(Integer, comment="""
带来属性提升的属性索引。
如果是初始属性，则该项为0。
如果基础属性，则此项为0。
如果是称号，则此项为1 2 3...。
如果是技能，则此项为1 2 3...。
如果是装备，则此项为1 2 3...。
    """)

    additional_property_type = Column(Integer,comment="参考AdditionalPropertyType")
    additional_property_value = Column(Integer,comment="对应type的value")

# 增

# 删

# 改

# 查

def get_properties_by_source_type_and_id(source_type: AdditionSourceType, source_id: int) -> List[InitialSkillAchievementEquipmentEtcPropertiesRecord]:
    """
    根据带来属性提升的物品类型和物品id查询对应的属性信息
    Args:
    session(Session): SQLAlchemy
    session对象
    source_type(int): 带来属性提升的物品类型
    source_id(int): 带来属性提升的物品id

    Returns:
    Optional[InitialSkillAchievementEquipmentEtcPropertiesRecord]: 如果找到了对应的属性信息，返回该对象，否则返回None
    """

    return session.query(InitialSkillAchievementEquipmentEtcPropertiesRecord).filter(
        InitialSkillAchievementEquipmentEtcPropertiesRecord.additional_source_type == source_type,
        InitialSkillAchievementEquipmentEtcPropertiesRecord.additional_source_id == source_id,
        InitialSkillAchievementEquipmentEtcPropertiesRecord.is_temp == False,
    ).all()

# other 
def get_properties_dict_by_source_type_and_source_id(*,source_type: AdditionSourceType, source_id: int):
    """
    :param source_type: 根据

    初始值（初始值id）
    技能（技能书id）
    成就（成就id，每个人只能有一个记录）
    穿戴装备（穿戴装备id）

    :param source_id:
    :return:
    """
    properties_dict = defaultdict(int)

    properties = get_properties_by_source_type_and_id(source_type,source_id)

    for one_property in properties:
        properties_dict[one_property.additional_property_type] += one_property.additional_property_value

    return properties_dict