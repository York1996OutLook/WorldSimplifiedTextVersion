from collections import defaultdict
from typing import Optional, DefaultDict, List

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session
from Enums import AdditionSourceType, AdditionalPropertyType, EquipmentPropertyAvailability, StuffType

Base = declarative_base()


class InitialSkillAchievementEquipmentPotionEtcPropertiesRecord(Base):
    """初始属性，基础属性加点、技能、装备(最大，最小，当前)、称号，临时药剂等常见的所有属性表，为永久表"""
    __tablename__ = 'initial_skill_achievement_equipment_etc_properties_record'

    id = Column(Integer, primary_key=True)

    additional_source_type = Column(Integer, comment="带来属性提升的物品类型，比如成就初始属性，基础属性加点，称号，技能，装备.参考枚举类型 AdditionSourceType")
    additional_source_id = Column(Integer, comment="""
带来属性提升的物品id。
如果是初始属性，则此项为空。
如果基础属性，则此项为character id。
如果是称号，则此项为achievement_id。
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
    property_availability = Column(Integer,
                                   comment="属性的类型，参考EquipmentPropertyAvailability。通常装备类型的属性才需要这个东西.表明是最低属性，最高属性还是当前属性")

    additional_property_type = Column(Integer, comment="参考AdditionalPropertyType")
    additional_property_value = Column(Integer, comment="对应参考AdditionalPropertyType的value")

    def __init__(self,
                 *,
                 additional_source_type: AdditionSourceType,

                 additional_property_type: AdditionalPropertyType,
                 additional_property_value: int,

                 additional_source_id: int = None,
                 additional_source_property_index: int = None,

                 property_availability: EquipmentPropertyAvailability = None,
                 ):
        """

        类型含义参考上面的comment字段
        :param additional_source_type:
        :param additional_source_id:
        :param additional_source_property_index:
        :param property_availability:
        :param additional_property_type:
        :param additional_property_value:
        """
        self.additional_source_type = additional_source_type
        self.additional_source_id = additional_source_id
        self.additional_source_property_index = additional_source_property_index
        self.property_availability = property_availability
        self.additional_property_type = additional_property_type
        self.additional_property_value = additional_property_value


# 增
def add_additional_property(
        *,
        additional_source_type: AdditionSourceType,
        additional_property_type: AdditionalPropertyType,
        additional_property_value: int,

        additional_source_id: int = None,
        additional_source_property_index: int = None,
        property_availability: EquipmentPropertyAvailability = None,
):
    record = InitialSkillAchievementEquipmentPotionEtcPropertiesRecord(
        additional_source_type=additional_source_type,
        additional_property_type=additional_property_type,
        additional_property_value=additional_property_value,
        additional_source_id=additional_source_id,
        additional_source_property_index=additional_source_property_index,
        property_availability=property_availability,
    )
    session.add(record)
    session.commit()


def add_base_property(
        *,
        character_id: int = None,

        base_property_type: AdditionalPropertyType,
        base_property_value: int,

):
    """
    新增一个基础属性
    :param character_id:
    :param base_property_type:
    :param base_property_value:
    :return:
    """
    add_additional_property(
        additional_source_id=character_id,

        additional_source_type=AdditionSourceType.BASE_PROPERTY_POINT,
        additional_property_type=base_property_type,
        additional_property_value=base_property_value,
    )


# 删
def del_achievement_properties(*,
                               achievement_id: int = None,
                               ):
    """
    删除成就对应的所有属性加成
    :param achievement_id:
    :return:
    """
    session.query(InitialSkillAchievementEquipmentPotionEtcPropertiesRecord).filter(
        InitialSkillAchievementEquipmentPotionEtcPropertiesRecord.additional_source_type == AdditionSourceType.ACHIEVEMENT,
        InitialSkillAchievementEquipmentPotionEtcPropertiesRecord.additional_source_id == achievement_id,
    ).delete(synchronize_session=False)

    session.commit()
    return True


# 改
def update_or_add_new_base_property(
        *,
        character_id: int,
        base_property_type: AdditionalPropertyType,
        base_property_value: int,
):
    if is_exists_by_base_property(character_id=character_id, base_property_type=base_property_type):
        update_base_property_by(character_id=character_id,
                                base_property_type=base_property_type,
                                base_property_value=base_property_value)
        return
    add_base_property(character_id=character_id,
                      base_property_type=base_property_type,
                      base_property_value=base_property_value)


def update_base_property_by(*,
                            character_id: int,
                            base_property_type: AdditionalPropertyType,
                            base_property_value: int,
                            ):
    """
    更新基础属性
    :param character_id:
    :param base_property_type:
    :param base_property_value:
    :return:
    """
    update_additional_property_by(
        source_type=AdditionSourceType.BASE_PROPERTY_POINT,
        source_id=character_id,
        additional_property_type=base_property_type,
        additional_property_value=base_property_value,
    )


def update_additional_property_by(
        *,
        source_type: AdditionSourceType,
        additional_property_type: AdditionalPropertyType,
        additional_property_value: int,

        source_id: int = None,
        additional_source_property_index: int = None,
        property_availability: EquipmentPropertyAvailability = None,

) -> InitialSkillAchievementEquipmentPotionEtcPropertiesRecord:
    """
    根据带来属性提升的物品类型和物品id查询对应的属性信息
    Args:
    source_type(int): 带来属性提升的物品类型
    additional_property_type(int): 属性类型
    additional_property_value(int): 属性值
    source_id(int): 带来属性提升的物品id
    additional_source_property_index:所属属性id。
    is_identify_temp: 是否是临时鉴定属性
    Returns:
    Optional[InitialSkillAchievementEquipmentEtcPropertiesRecord]: 如果找到了对应的属性信息，返回该对象，否则返回None
    """
    query = session.query(InitialSkillAchievementEquipmentPotionEtcPropertiesRecord).filter(
        InitialSkillAchievementEquipmentPotionEtcPropertiesRecord.additional_source_type == source_type,
        InitialSkillAchievementEquipmentPotionEtcPropertiesRecord.additional_property_type == additional_property_type,
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

    record = query.first()
    record.additional_property_value = additional_property_value
    session.commit()
    return record


# 查
def is_exists_by_base_property(*,
                               character_id: int,
                               base_property_type: AdditionalPropertyType,
                               ):
    query = session.query(InitialSkillAchievementEquipmentPotionEtcPropertiesRecord).filter(
        InitialSkillAchievementEquipmentPotionEtcPropertiesRecord.additional_source_id == character_id,
        InitialSkillAchievementEquipmentPotionEtcPropertiesRecord.additional_property_type == base_property_type,
    ).first()
    return query is not None


def is_exists_by_properties_additional_source_type_additional_property_type(
        *,
        additional_source_type: AdditionSourceType,
        additional_property_type: AdditionalPropertyType,
):
    """
    根据附加属性来源的类型和属性类型查询是否存在对应属性记录；
    :param additional_source_type:
    :param additional_property_type:
    :return:
    """
    query = session.query(InitialSkillAchievementEquipmentPotionEtcPropertiesRecord).filter(
        InitialSkillAchievementEquipmentPotionEtcPropertiesRecord.additional_source_type == additional_source_type,
        InitialSkillAchievementEquipmentPotionEtcPropertiesRecord.additional_property_type == additional_property_type,
    ).first()
    return query is not None


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

                           additional_property_type: AdditionalPropertyType = None, ) -> DefaultDict[int, int]:
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


def get_properties_dict_by_initial() -> DefaultDict[int, int]:
    """
    获取初始属性。分开写函数，减少错误发生
    :return:
    """
    properties_dict = get_properties_dict_by(source_type=AdditionSourceType.INITIAL)
    return properties_dict


def get_properties_dict_by_achievement_id(*,
                                          achievement_id: int,
                                          ) -> DefaultDict[int, int]:
    """
    获取成就称号对应的属性。分开写函数，减少错误发生
    :return:
    """
    properties_dict = get_properties_dict_by(
        source_type=AdditionSourceType.ACHIEVEMENT,
        source_id=achievement_id,
    )
    return properties_dict


def get_base_property_dict_by(*,
                              character_id: int,
                              ) -> DefaultDict[int, int]:
    """
    获取基础属性对应的属性。分开写函数，减少错误发生
    :return:
    """
    properties_dict = get_properties_dict_by(
        source_type=AdditionSourceType.BASE_PROPERTY_POINT,
        source_id=character_id,
    )
    return properties_dict


def get_used_base_property_points_num(character_id: int,
                                      ) -> int:
    """
    获取已经使用的基础点数数量
    :param character_id:
    :return:
    """
    properties_dict = get_base_property_dict_by(character_id=character_id)
    used_points = 0
    for key in properties_dict:
        used_points += properties_dict[key]
    return used_points


def get_properties_dict_by_skill(*,
                                 skill_book_id: int,
                                 ) -> DefaultDict[int, int]:
    """
    获取基础属性对应的属性。分开写函数，减少错误发生
    :return:
    """
    properties_dict = get_properties_dict_by(
        source_type=AdditionSourceType.SKILL,
        source_id=skill_book_id,
    )
    return properties_dict


def get_properties_dict_by_equipment_record(*,
                                            stuff_record_id: int,
                                            ) -> DefaultDict[int, int]:
    """
    获取基础属性对应的属性。分开写函数，减少错误发生
    :return:
    """
    properties_dict = get_properties_dict_by(
        source_type=AdditionSourceType.EQUIPMENT_RECORD,
        source_id=stuff_record_id,
        property_availability=EquipmentPropertyAvailability.CURRENT,
    )
    return properties_dict


def get_properties_dict_by_potion(*,
                                  potion_id: int,
                                  ) -> DefaultDict[int, int]:
    """
    获取基础属性对应的属性。分开写函数，减少错误发生
    :return:
    """
    properties_dict = get_properties_dict_by(
        source_type=AdditionSourceType.POTION,
        source_id=potion_id,
    )
    return properties_dict


if __name__ == '__main__':
    # 录入初始属性
    player_initial_properties_list = [
        {
            # base
            "additional_property_type": AdditionalPropertyType.ATTACK,
            "additional_property_value": 10,
        },
        {
            # base
            "additional_property_type": AdditionalPropertyType.ATTACK_SPEED,
            "additional_property_value": 10,
        },
        {
            # base
            "additional_property_type": AdditionalPropertyType.HEALTH,
            "additional_property_value": 100,
        },
        {
            # base
            "additional_property_type": AdditionalPropertyType.MANA,
            "additional_property_value": 100,
        },
    ]

    for player_initial_property in player_initial_properties_list:
        # 如果已经添加过了，则进行更新。否则，新建；
        if is_exists_by_properties_additional_source_type_additional_property_type(
                additional_source_type=AdditionSourceType.INITIAL,
                additional_property_type=player_initial_property['additional_property_type'],
        ):
            # 如果存在则更新
            update_additional_property_by(
                source_type=AdditionSourceType.INITIAL,
                additional_property_type=player_initial_property['additional_property_type'],
                additional_property_value=player_initial_property['additional_property_value'],
            )
        else:
            # 添加新的初始属性
            add_additional_property(additional_source_type=AdditionSourceType.INITIAL,
                                    additional_property_type=player_initial_property['additional_property_type'],
                                    additional_property_value=player_initial_property['additional_property_value']
                                    )
