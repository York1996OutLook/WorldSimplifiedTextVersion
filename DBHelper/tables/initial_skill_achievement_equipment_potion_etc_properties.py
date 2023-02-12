from collections import defaultdict
from typing import Optional, DefaultDict, List

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session
from Enums import AdditionSourceType, AdditionalPropertyType, EquipmentPropertyAvailability

Base = declarative_base()


class InitialSkillAchievementEquipmentPotionEtcPropertiesRecord(Base):
    """初始属性，基础属性加点、技能、装备(最大，最小，当前)、称号，临时药剂等常见的所有属性表，为永久表"""
    __tablename__ = 'initial_skill_achievement_equipment_etc_properties_record'

    id = Column(Integer, primary_key=True)

    additional_source_type = Column(Integer, comment="带来属性提升的物品类型，比如成就初始属性，基础属性加点，称号，技能，装备")
    additional_source_id = Column(Integer, comment="""
带来属性提升的物品id。
如果是初始属性，则此项为空。
如果基础属性，则此项为character id。
如果是称号，则此项为character_id。
如果是技能，则此项为skill_book_id。
如果是装备，则此项为stuff_record_id。
如果是药剂，则此项为potion_id。
    """)

    additional_source_property_index = Column(Integer, comment="""
带来属性提升的属性索引。

如果是初始属性，则该项为0。
如果基础属性，则此项为0。
如果是称号，则此项为1 2 3...。
如果是技能，则此项为1 2 3...。
如果是装备，则此项为1 2 3...。
如果是药剂，则此项为1 2 3...。
    """)
    property_availability = Column(Integer, comment="属性的类型，参考EquipmentPropertyAvailability。通常装备类型的属性才需要这个东西")

    additional_property_type = Column(Integer, comment="参考AdditionalPropertyType")
    additional_property_value = Column(Integer, comment="对应参考AdditionalPropertyType的value")


# 增

# 删

# 改

# 查


def get_properties_by(
        *,
        source_type: AdditionSourceType,
        source_id: int = None,

        additional_source_property_index: int = None,
        property_availability: EquipmentPropertyAvailability = None,

        additional_property_type: AdditionalPropertyType = None,
) -> List[InitialSkillAchievementEquipmentPotionEtcPropertiesRecord]:
    """
    根据带来属性提升的物品类型和物品id查询对应的属性信息
    Args:
    source_type(int): 带来属性提升的物品类型
    source_id(int): 带来属性提升的物品id
    additional_source_property_index:所属属性id。
    is_identify_temp: 是否是临时鉴定属性
    Returns:
    Optional[InitialSkillAchievementEquipmentEtcPropertiesRecord]: 如果找到了对应的属性信息，返回该对象，否则返回None
    """
    query = session.query(InitialSkillAchievementEquipmentPotionEtcPropertiesRecord).filter(
        InitialSkillAchievementEquipmentPotionEtcPropertiesRecord.additional_source_type == source_type,
    )
    if source_id:
        query = query.filter(
            InitialSkillAchievementEquipmentPotionEtcPropertiesRecord.additional_source_id == source_id,
        )
    if additional_source_property_index:
        query = query.filter(
            InitialSkillAchievementEquipmentPotionEtcPropertiesRecord.additional_source_property_index == additional_source_property_index,
        )
    if property_availability:
        query = query.filter(
            InitialSkillAchievementEquipmentPotionEtcPropertiesRecord.property_availability == property_availability,
        )
    if additional_property_type:
        query = query.filter(
            InitialSkillAchievementEquipmentPotionEtcPropertiesRecord.additional_property_type == additional_property_type,
        )
    return query.all()


# other
def get_properties_dict_by(*,
                           source_type: AdditionSourceType,
                           source_id: int = None,

                           additional_source_property_index: int = None,
                           property_availability: EquipmentPropertyAvailability = None,

                           additional_property_type: AdditionalPropertyType = None, ):
    """
    转换成字典；
    :param source_type:
    :param source_id:
    :param additional_source_property_index:
    :param property_availability:
    :param additional_property_type:
    :return:
    """
    properties_dict = defaultdict(int)

    properties = get_properties_by(source_type=source_type,
                                   source_id=source_id,
                                   additional_source_property_index=additional_source_property_index,
                                   property_availability=property_availability,
                                   additional_property_type=additional_property_type,
                                   )
    for one_property in properties:
        properties_dict[one_property.additional_property_type] += one_property.additional_property_value

    return properties_dict
