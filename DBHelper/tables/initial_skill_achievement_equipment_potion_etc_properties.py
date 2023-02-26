from collections import defaultdict
import os.path as osp
from typing import Optional, DefaultDict, List

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session
from Enums import AdditionSourceType, AdditionalPropertyType, EquipmentPropertyAvailability, StuffType, \
    property_cn_type_dict
import local_setting
from Utils import tools

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
def add(
        *,
        additional_source_type: AdditionSourceType,
        additional_property_type: AdditionalPropertyType,
        additional_property_value: int,

        additional_source_id: int = None,
        additional_source_property_index: int = None,
        property_availability: EquipmentPropertyAvailability = None,
) -> InitialSkillAchievementEquipmentPotionEtcPropertiesRecord:
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
    return InitialSkillAchievementEquipmentPotionEtcPropertiesRecord


def add_initial_properties(*,
                           additional_property_type: AdditionalPropertyType,
                           additional_property_value: int,

                           ):
    add(additional_source_type=AdditionSourceType.INITIAL,
        additional_property_type=additional_property_type,
        additional_property_value=additional_property_value)


def add_monster_properties(*,
                           additional_property_type: AdditionalPropertyType,
                           additional_property_value: int,
                           ):
    add(additional_source_type=AdditionSourceType.MONSTER,
        additional_property_type=additional_property_type,
        additional_property_value=additional_property_value)


def add_base_additional_properties(*,
                                   base_property_type: AdditionalPropertyType,
                                   additional_property_type: AdditionalPropertyType,
                                   additional_property_value: int):
    """

    :param base_property_type: 基础属性值。作为additional_source_id存到表格中；
    :param additional_property_type: 基础属性增加的其它的额外属性
    :param additional_property_value: 其它额外属性的值
    :return:
    """
    add(additional_source_type=AdditionSourceType.BASE_ADDITIONAL,
        additional_source_id=base_property_type,
        additional_property_type=additional_property_type,
        additional_property_value=additional_property_value)


def add_equipment_properties(*,
                             additional_property_type: AdditionalPropertyType,
                             additional_property_value: int,

                             achievement_id: int = None,
                             property_index: int = None,
                             property_availability: EquipmentPropertyAvailability = None,
                             ):
    record = add(
        additional_source_type=AdditionSourceType.EQUIPMENT_PROTOTYPE,
        additional_property_type=additional_property_type,
        additional_property_value=additional_property_value,
        additional_source_id=achievement_id,
        additional_source_property_index=property_index,
        property_availability=property_availability,
    )
    return record


def add_achievement_properties(*,
                               achievement_id: int,
                               additional_source_property_index: int,
                               additional_property_type: AdditionalPropertyType,
                               additional_property_value: int,
                               ):
    add(
        additional_source_type=AdditionSourceType.ACHIEVEMENT,
        additional_property_type=additional_property_type,
        additional_property_value=additional_property_value,
        additional_source_id=achievement_id,
        additional_source_property_index=additional_source_property_index,
    )


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
    add(
        additional_source_id=character_id,

        additional_source_type=AdditionSourceType.BASE_PROPERTY_POINT,
        additional_property_type=base_property_type,
        additional_property_value=base_property_value,
    )


# 删

def del_initial_properties() -> bool:
    """
    删除成就对应的所有属性加成
    :return:
    """
    session.query(InitialSkillAchievementEquipmentPotionEtcPropertiesRecord).filter(
        InitialSkillAchievementEquipmentPotionEtcPropertiesRecord.additional_source_type == AdditionSourceType.INITIAL,
    ).delete(synchronize_session=False)

    session.commit()
    return True


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


def del_equipment_prototype_properties(*,
                                       equipment_id: int,
                                       ):
    """
    删除某个装备原型的所有属性。
    :param equipment_id:
    :return:
    """
    session.query(InitialSkillAchievementEquipmentPotionEtcPropertiesRecord).filter(
        InitialSkillAchievementEquipmentPotionEtcPropertiesRecord.additional_source_type == AdditionSourceType.EQUIPMENT_PROTOTYPE,
        InitialSkillAchievementEquipmentPotionEtcPropertiesRecord.additional_source_id == equipment_id,
    ).delete(synchronize_session=False)

    session.commit()
    return True


def del_monster_prototype_properties(*,
                                     monster_id: int,
                                     ):
    """
    删除某个装备原型的所有属性。
    :param monster_id:
    :return:
    """
    session.query(InitialSkillAchievementEquipmentPotionEtcPropertiesRecord).filter(
        InitialSkillAchievementEquipmentPotionEtcPropertiesRecord.additional_source_type == AdditionSourceType.EQUIPMENT_PROTOTYPE,
        InitialSkillAchievementEquipmentPotionEtcPropertiesRecord.additional_source_id == monster_id,
    ).delete(synchronize_session=False)

    session.commit()
    return True


def del_base_additional_properties(*,
                                   base_property_type: AdditionalPropertyType, ):
    session.query(InitialSkillAchievementEquipmentPotionEtcPropertiesRecord).filter(
        InitialSkillAchievementEquipmentPotionEtcPropertiesRecord.additional_source_type == AdditionSourceType.BASE_ADDITIONAL,
        InitialSkillAchievementEquipmentPotionEtcPropertiesRecord.additional_source_id == base_property_type,
    ).delete()
    session.commit()


# 改

# def update_base_additional_properties(*,
#                                       base_property_type: AdditionalPropertyType,
#                                       additional_property_type: AdditionalPropertyType,
#                                       additional_property_value: int):
#     record = session.query(InitialSkillAchievementEquipmentPotionEtcPropertiesRecord).filter(
#         InitialSkillAchievementEquipmentPotionEtcPropertiesRecord.additional_source_type == AdditionSourceType.BASE_ADDITIONAL,
#         InitialSkillAchievementEquipmentPotionEtcPropertiesRecord.additional_source_id == base_property_type,
#         InitialSkillAchievementEquipmentPotionEtcPropertiesRecord.additional_property_type == additional_property_type,
#     ).first()
#     record.additional_property_value = additional_property_value


def update_or_add_new_base_property(
        *,
        character_id: int,
        base_property_type: AdditionalPropertyType,
        base_property_value: int,
):
    """
    更新基础属性。
    :param character_id:
    :param base_property_type:
    :param base_property_value:
    :return:
    """
    if is_exists_by_base_property(character_id=character_id, base_property_type=base_property_type):
        return update_base_property_by(character_id=character_id,
                                       base_property_type=base_property_type,
                                       base_property_value=base_property_value)

    return add_base_property(character_id=character_id,
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
    update_by(
        source_type=AdditionSourceType.BASE_PROPERTY_POINT,
        source_id=character_id,
        additional_property_type=base_property_type,
        additional_property_value=base_property_value,
    )


def update_by(
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
    session.refresh(record)
    return record


def update_player_property(
        *,
        character_id: int = None,

        additional_property_type: AdditionalPropertyType,
        additional_property_value: int,
):
    return update_by(source_type=AdditionSourceType.PLAYER,
                     additional_property_type=additional_property_type,
                     additional_property_value=additional_property_value,
                     source_id=character_id)


def update_player_properties_dict(*,
                                  character_id: int = None,
                                  properties_dict: DefaultDict[int, int]
                                  ):
    for property_type_key in properties_dict:
        update_player_property(
            character_id=character_id,
            additional_property_type=property_type_key,
            additional_property_value=properties_dict[property_type_key],
        )


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


def get_base_property_dict_by_character_id(*,
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


def get_used_base_property_points_num_by_character_id(character_id: int,
                                                      ) -> int:
    """
    获取已经使用的基础点数数量
    :param character_id:
    :return:
    """
    properties_dict = get_base_property_dict_by_character_id(character_id=character_id)
    used_points = 0
    for key in properties_dict:
        used_points += properties_dict[key]
    return used_points


def get_additional_property_dict_by_base_property(*,
                                             base_property_type: AdditionalPropertyType,
                                             ):
    records = session.query(InitialSkillAchievementEquipmentPotionEtcPropertiesRecord).filter(
        InitialSkillAchievementEquipmentPotionEtcPropertiesRecord.additional_source_type == AdditionSourceType.BASE_ADDITIONAL,
        InitialSkillAchievementEquipmentPotionEtcPropertiesRecord.additional_source_id == base_property_type,
    ).all()

    property_dict=defaultdict(int)
    for record in records:
        property_dict[record.additional_property_type]=record.additional_property_value
    return property_dict


def get_properties_dict_by_skill_book_id(*,
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
                                            equipment_record_id: int,
                                            ) -> DefaultDict[int, int]:
    """
    获取基础属性对应的属性。分开写函数，减少错误发生
    :return:
    """
    properties_dict = get_properties_dict_by(
        source_type=AdditionSourceType.EQUIPMENT_RECORD,
        source_id=equipment_record_id,
        property_availability=EquipmentPropertyAvailability.CURRENT,
    )
    return properties_dict


def get_properties_dict_by_potion_id(*,
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


# other

def insert_initial_properties():
    # 录入初始属性
    json_src = osp.join(local_setting.json_data_root, 'initial_properties', 'initial_properties.json')
    properties_dict_list = tools.file2dict_list(src=json_src)

    # 删除所有初始属性后再进行添加；
    del_initial_properties()
    for player_initial_property_dict in properties_dict_list:
        property_type_cn = player_initial_property_dict['属性']
        property_type = property_cn_type_dict[property_type_cn]
        property_value = player_initial_property_dict['属性值']
        # 添加新的初始属性
        add_initial_properties(
            additional_property_type=property_type,
            additional_property_value=property_value,
        )


def insert_base_additional_properties():
    base_property_additional_property_json_src = osp.join(local_setting.json_data_root, "properties",
                                                          'base_property_additional_properties.json')
    addition_dict_list = tools.file2dict_list(src=base_property_additional_property_json_src)
    for addition_dict in addition_dict_list:
        base_property_type_cn = addition_dict['基础属性名称']
        base_property_type = property_cn_type_dict[base_property_type_cn]

        attack_addition = addition_dict['攻击力增加']
        attack_speed_addition = addition_dict['出手速度增加']

        health_addition = addition_dict['生命值增加']
        mana_addition = addition_dict['法力值增加']

        # 先删除基础属性对应的额外属性增加值，再添加；
        del_base_additional_properties(base_property_type=base_property_type)
        add_base_additional_properties(base_property_type=base_property_type,
                                       additional_property_type=AdditionalPropertyType.ATTACK,
                                       additional_property_value=attack_addition
                                       )
        add_base_additional_properties(base_property_type=base_property_type,
                                       additional_property_type=AdditionalPropertyType.ATTACK_SPEED,
                                       additional_property_value=attack_speed_addition
                                       )
        add_base_additional_properties(base_property_type=base_property_type,
                                       additional_property_type=AdditionalPropertyType.HEALTH,
                                       additional_property_value=health_addition
                                       )
        add_base_additional_properties(base_property_type=base_property_type,
                                       additional_property_type=AdditionalPropertyType.MANA,
                                       additional_property_value=mana_addition
                                       )


if __name__ == '__main__':
    insert_initial_properties()
    insert_base_additional_properties()
