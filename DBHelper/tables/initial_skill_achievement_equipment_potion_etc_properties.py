from collections import defaultdict
import os.path as osp
from typing import Optional, DefaultDict, List

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session
from DBHelper.tables.base_table import Basic, Base
from Enums import AdditionSourceType, AdditionalPropertyType, EquipmentPropertyAvailability, StuffType
import local_setting
from Utils import tools


class InitialSkillAchievementEquipmentPotionEtcPropertiesRecord(Basic, Base):
    """初始属性，基础属性加点、技能、装备(最大，最小，当前)、称号，临时药剂等常见的所有属性表，为永久表"""
    __tablename__ = 'initial_skill_achievement_equipment_etc_properties_record'

    additional_source_type = Column(Integer, comment="带来属性提升的物品类型，比如成就初始属性，基础属性加点，称号，技能，装备.参考枚举类型 AdditionSourceType")
    additional_source_id = Column(Integer, comment="""
带来属性提升的物品id。
如果是初始属性，则此项为空。
如果基础属性，则此项为character id。
如果是称号，则此项为achievement_id。
如果是技能，则此项为skill_book_id。
如果是装备，则此项为stuff_record_id。
如果是药剂，则此项为potion_id。
如果是状态，则此项为status_id。
    """)

    additional_source_property_index = Column(Integer, comment="""
带来属性提升的属性索引。

如果是初始属性，则该项为0。
如果基础属性，则此项为0。
如果是称号，则此项为1 2 3...。
如果是技能，则此项为1 2 3...。
如果是装备，则此项为1 2 3...。
如果是药剂，则此项为1 2 3...。
如果是状态，则此项为1 2 3...。
    """)
    property_availability = Column(Integer,
                                   comment="属性的类型，参考EquipmentPropertyAvailability。"
                                           "对于装备来说：表明是最低属性，最高属性还是当前属性"
                                           "对于技能来说，这个属性为作用的对象，自身或者是敌人")

    additional_property_type = Column(Integer, comment="参考AdditionalPropertyType")
    additional_property_value = Column(Integer, comment="对应参考AdditionalPropertyType的value")

    @classmethod
    def add_or_update_by_id(cls,
                            *,
                            _id: int,
                            additional_source_type: int = None,

                            additional_property_type: int = None,
                            additional_property_value: int = None,

                            additional_source_id: int = None,
                            additional_source_property_index: int = None,

                            property_availability: int = None,
                            ):
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
        return record

    @classmethod
    def get_properties_by_skill_book_id(cls,
                                        *,
                                        skill_book_id: int,
                                        ):
        properties = get_properties_by(source_type=AdditionSourceType.SKILL_BOOK.index, source_id=skill_book_id)
        return properties

    # 增
    @classmethod
    def add(cls,
            additional_source_type: int = None,
            additional_source_id: int = None,

            additional_property_type: int = None,
            additional_property_value: int = None,

            additional_source_property_index: int = None,

            property_availability: int = None, ):
        fields = cls.update_fields_from_signature(func=cls.add)
        record = cls.add_with_kwargs(**fields)
        return record

    @classmethod
    def add_player_properties(cls,
                              *,
                              character_id: int,
                              additional_property_type: int,
                              additional_property_value: int,
                              ):
        record = cls.add(additional_source_type=AdditionSourceType.PLAYER.index,
                         additional_source_id=character_id,
                         additional_property_type=additional_property_type,
                         additional_property_value=additional_property_value,
                         )
        return record

    @classmethod
    def add_initial_properties(cls,
                               *,
                               additional_property_type: int,
                               additional_property_value: int,
                               ):
        record = cls.add(additional_source_type=AdditionSourceType.INITIAL.index,
                         additional_property_type=additional_property_type,
                         additional_property_value=additional_property_value,
                         )
        return record

    @classmethod
    def add_monster_properties(cls, *,
                               monster_id: int,
                               additional_property_type: int,
                               additional_property_value: int,
                               ):
        record = cls.add(additional_source_type=AdditionSourceType.MONSTER.index,
                         additional_source_id=monster_id,
                         additional_property_type=additional_property_type,
                         additional_property_value=additional_property_value,
                         )
        return record

    @classmethod
    def add_base_additional_properties(cls,
                                       *,
                                       base_property_type: int,
                                       additional_source_property_index: int,
                                       additional_property_type: int,
                                       additional_property_value: int):
        """

        :param base_property_type: 基础属性值。作为additional_source_id存到表格中；
        :param additional_source_property_index: 属性索引
        :param additional_property_type: 基础属性增加的其它的额外属性
        :param additional_property_value: 其它额外属性的值
        :return:
        """
        record = cls.add(additional_source_type=AdditionSourceType.BASE_ADDITIONAL.index,
                         additional_source_id=base_property_type,
                         additional_source_property_index=additional_source_property_index,
                         additional_property_type=additional_property_type,
                         additional_property_value=additional_property_value,
                         )
        return record

    @classmethod
    def add_equipment_properties(cls,
                                 *,
                                 equipment_stuff_id: int,
                                 additional_source_property_index: int,

                                 property_availability: int = None,
                                 additional_property_type: int = None,
                                 additional_property_value: int = None,
                                 ):
        record = cls.add(additional_source_type=AdditionSourceType.EQUIPMENT_PROTOTYPE.index,
                         additional_source_id=equipment_stuff_id,
                         additional_source_property_index=additional_source_property_index,
                         property_availability=property_availability,
                         additional_property_type=additional_property_type,
                         additional_property_value=additional_property_value,
                         )
        return record

    @classmethod
    def add_achievement_properties(cls,
                                   *,
                                   achievement_id: int,
                                   additional_source_property_index: int,
                                   additional_property_type: int,
                                   additional_property_value: int,
                                   ):
        record = cls.add_with_kwargs(additional_source_type=AdditionSourceType.ACHIEVEMENT_TITLE.index,
                                     additional_source_id=achievement_id,
                                     additional_source_property_index=additional_source_property_index,
                                     additional_property_type=additional_property_type,
                                     additional_property_value=additional_property_value,
                                     )
        return record

    # 删
    @classmethod
    def del_initial_properties(cls) -> bool:
        """
        删除成就对应的所有属性加成
        :return:
        """
        result = cls.del_all_by_kwargs(additional_source_type=AdditionSourceType.INITIAL.index)
        return result

    @classmethod
    def del_achievement_properties(cls,
                                   *,
                                   achievement_id: int = None,
                                   ) -> bool:
        """
        删除成就对应的所有属性加成
        :param achievement_id:
        :return:
        """
        result = cls.del_all_by_kwargs(additional_source_type=AdditionSourceType.ACHIEVEMENT_TITLE.index,
                                       additional_source_id=achievement_id)
        return result

    @classmethod
    def del_equipment_prototype_properties(cls,
                                           *,
                                           equipment_id: int,
                                           ) -> bool:
        """
        删除某个装备原型的所有属性。
        :param equipment_id:
        :return:
        """
        result = cls.del_all_by_kwargs(additional_source_type=AdditionSourceType.EQUIPMENT_PROTOTYPE.index,
                                       additional_source_id=equipment_id)
        return result

    @classmethod
    def del_monster_prototype_properties(cls,
                                         *,
                                         monster_id: int,
                                         ) -> bool:
        """
        删除某个装备原型的所有属性。
        :param monster_id:
        :return:
        """
        result = cls.del_all_by_kwargs(additional_source_type=AdditionSourceType.MONSTER.index,
                                       additional_source_id=monster_id)
        return result

    @classmethod
    def del_skill_book_properties(cls,
                                  *,
                                  skill_book_id: int,
                                  ) -> bool:
        """
        删除某个装备原型的所有属性。
        :param skill_book_id:
        :return:
        """

        result = cls.del_all_by_kwargs(additional_source_type=AdditionSourceType.SKILL_BOOK.index,
                                       additional_source_id=skill_book_id)
        return result

    @classmethod
    def del_status_properties(cls,
                              *,
                              status_id: int,
                              ) -> bool:
        """
        删除某个装备原型的所有属性。
        :param status_id:
        :return:
        """
        result = cls.del_all_by_kwargs(additional_source_type=AdditionSourceType.STATUS.index,
                                       additional_source_id=status_id)
        return result

    @classmethod
    def del_base_additional_properties(cls,
                                       *,
                                       base_property_type: int,
                                       ) -> bool:
        result = cls.del_all_by_kwargs(additional_source_type=AdditionSourceType.BASE_ADDITIONAL.index,
                                       additional_source_id=base_property_type)
        return result

    # 改
    @classmethod
    def update_base_additional_properties(cls,
                                          *,
                                          base_property_type: int,
                                          additional_property_type: int,

                                          additional_property_value: int
                                          ) -> "InitialSkillAchievementEquipmentPotionEtcPropertiesRecord":
        query_dict = {
            'additional_source_type': AdditionSourceType.BASE_ADDITIONAL.index,
            'base_property_type': base_property_type,
            'additional_property_type': additional_property_type,
        }
        update_dict = {
            "additional_property_value": additional_property_value
        }
        record = cls.update_fields_by_query_dict(query_dict=query_dict, update_dict=update_dict)

        return record

    @classmethod
    def update_player_base_property_by(cls,
                                       *,
                                       character_id: int,
                                       base_property_type: int,
                                       base_property_value: int,
                                       ):
        """
        更新基础属性
        :param character_id:
        :param base_property_type:
        :param base_property_value:
        :return:
        """
        query_dict = {
            'additional_source_type': AdditionSourceType.BASE_PROPERTY_POINT.index,
            'additional_source_id': character_id,

            'additional_property_type': base_property_type,
        }
        update_dict = {
            "additional_property_value": base_property_value
        }
        record = cls.update_fields_by_query_dict(query_dict=query_dict, update_dict=update_dict)
        return record

    @classmethod
    def update_player_property(cls,
                               *,
                               character_id: int = None,

                               additional_property_type: int,
                               additional_property_value: int,
                               ) -> cls:
        query_dict = {
            'additional_source_type': AdditionSourceType.PLAYER.index,
            'additional_source_id': character_id,
            'additional_property_type': additional_property_type,
        }
        update_dict = {
            "additional_property_value": additional_property_value
        }
        record = cls.update_fields_by_query_dict(query_dict=query_dict, update_dict=update_dict)
        return record

    @classmethod
    def update_skill_property(cls,

                              *,
                              skill_id: int,
                              property_index: int,
                              additional_property_type: int,
                              additional_property_value: int,
                              ):
        """
        :param skill_id:    技能id
        :param property_index:  属性的id。第一条属性，第二条属性，第三条属性，第四条属性
        :param additional_property_type: 属性的类型
        :param additional_property_value:   属性值
        :return:
        """
        ...

    @classmethod
    def update_skill_book_property(cls,
                                   *,
                                   skill_book_id: int = None,
                                   property_index: int,
                                   property_target: int,
                                   additional_property_type: int,
                                   additional_property_value: int,
                                   ):
        """
        :param skill_book_id:    技能id
        :param property_index:  属性的id。第一条属性，第二条属性，第三条属性，第四条属性
        :param property_target: 属性的作用对象。对于被动技能来说，作用对象是自己，对于主动技能，作用对象可能是自己也可能是对方；
        :param additional_property_type: 属性的类型
        :param additional_property_value:   属性值
        :return:
        """
        ...

    @classmethod
    def update_player_properties_dict(cls,
                                      *,
                                      character_id: int = None,
                                      properties_dict: DefaultDict[int, int]
                                      ):
        """
        更新用户的属性
        :param character_id:
        :param properties_dict:
        :return:
        """
        ...

    # 查
    @classmethod
    def is_exists(cls,
                  *,
                  additional_source_type: int = None,
                  additional_source_id: int = None,
                  additional_source_property_index: int = None,
                  property_availability: int = None,
                  additional_property_type: int = None,
                  ):
        fields = cls.update_fields_from_signature(func=cls.is_exists)
        result = cls.is_exists_by_kwargs(**fields)
        return result

    @classmethod
    def get_properties_by(cls,
                          *,
                          additional_source_type: int,
                          additional_source_id: int = None,

                          additional_source_property_index: int = None,
                          property_availability: EquipmentPropertyAvailability = None,

                          additional_property_type: int = None,
                          ) -> List["InitialSkillAchievementEquipmentPotionEtcPropertiesRecord"]:

        fields = cls.update_fields_from_signature(func=cls.is_exists)
        records=cls.get_all_by(**fields)

        return records


# other
def get_properties_dict_by(*,
                           source_type: int,
                           source_id: int = None,

                           additional_source_property_index: int = None,
                           property_availability: EquipmentPropertyAvailability = None,

                           additional_property_type: int = None, ) -> DefaultDict[
    int, int]:
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
    properties_dict = get_properties_dict_by(source_type=AdditionSourceType.INITIAL.index)
    return properties_dict


def get_properties_dict_by_achievement_id(*,
                                          achievement_id: int,
                                          ) -> DefaultDict[int, int]:
    """
    获取成就称号对应的属性。分开写函数，减少错误发生
    :return:
    """
    properties_dict = get_properties_dict_by(
        source_type=AdditionSourceType.ACHIEVEMENT_TITLE.index,
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


def get_property_dict_by_skill_id(*,
                                  skill_id: int,
                                  ) -> DefaultDict[int, int]:
    """
    获取基础属性对应的属性。分开写函数，减少错误发生
    :return:
    """
    properties_dict = get_properties_dict_by(
        source_type=AdditionSourceType.SKILL.index,
        source_id=skill_id,
    )
    return properties_dict


def get_property_dict_by_monster_id(*,
                                    monster_id: int,
                                    ) -> DefaultDict[int, int]:
    """
    获取基础属性对应的属性。分开写函数，减少错误发生
    :return:
    """
    properties_dict = get_properties_dict_by(
        source_type=AdditionSourceType.MONSTER.index,
        source_id=monster_id,
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
                                                  base_property_type: int,
                                                  ) -> DefaultDict[int, int]:
    records = session.query(InitialSkillAchievementEquipmentPotionEtcPropertiesRecord).filter(
        InitialSkillAchievementEquipmentPotionEtcPropertiesRecord.additional_source_type == AdditionSourceType.BASE_ADDITIONAL.index,
        InitialSkillAchievementEquipmentPotionEtcPropertiesRecord.additional_source_id == base_property_type,
    ).all()

    property_dict = defaultdict(int)
    for record in records:
        property_dict[record.additional_property_type] = record.additional_property_value
    return property_dict


def get_properties_by_status_id(*,
                                status_id: int,
                                ):
    properties = get_properties_by(source_type=AdditionSourceType.STATUS.index, source_id=status_id)
    return properties


def get_properties_by_base_property(*,
                                    base_property_id: int,
                                    ):
    properties = get_properties_by(source_type=AdditionSourceType.BASE_ADDITIONAL.index,
                                   source_id=base_property_id)
    return properties


def get_properties_by_achievement_id(*,
                                     achievement_id: int,
                                     ):
    properties = get_properties_by(source_type=AdditionSourceType.ACHIEVEMENT_TITLE.index,
                                   source_id=achievement_id)
    return properties


def get_properties_dict_by_skill_book_id(*,
                                         skill_book_id: int,
                                         ) -> DefaultDict[int, int]:
    """
    获取基础属性对应的属性。分开写函数，减少错误发生
    :return:
    """
    properties_dict = get_properties_dict_by(
        source_type=AdditionSourceType.SKILL.index,
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
        source_type=AdditionSourceType.EQUIPMENT_RECORD.index,
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
        source_type=AdditionSourceType.POTION.index,
        source_id=potion_id,
    )
    return properties_dict


# other

def add_skill_book_properties(*,
                              skill_book_id: int,
                              property_index: int,
                              property_target: int,
                              property_type: int,
                              property_value: int):
    """
    新增skill book对应的一条属性
    :param skill_book_id: 技能书的id
    :param property_index: 技能的索引
    :param property_target: 属性的作用对象
    :param property_type: 属性的类型
    :param property_value: 属性的值
    :return:
    :rtype:
    """
    skill_book_property = add(additional_source_type=AdditionSourceType.SKILL_BOOK.index,

                              additional_source_id=skill_book_id,
                              additional_source_property_index=property_index,
                              property_availability=property_target,
                              additional_property_type=property_type,
                              additional_property_value=property_value,
                              )
    return skill_book_property


def add_status_properties(*,
                          status_id: int,
                          property_index: int,
                          property_type: int,
                          property_value: int):
    """
    新增 状态 对应的一条属性
    :param status_id: 状态id
    :param property_index: 技能的索引
    :param property_type: 属性的类型
    :param property_value: 属性的值
    :return:
    :rtype:
    """
    skill_book_property = add(additional_source_type=AdditionSourceType.STATUS.index,
                              additional_source_id=status_id,
                              additional_source_property_index=property_index,
                              additional_property_type=property_type,
                              additional_property_value=property_value,
                              )
    return skill_book_property


def insert_initial_properties(*, verbose: bool = False):
    # 录入初始属性
    json_src = osp.join(local_setting.json_data_root, 'properties', 'initial_properties.json')
    properties_dict_list = tools.file2dict_list(src=json_src)

    # 删除所有初始属性后再进行添加；
    del_initial_properties()
    if verbose:
        print("删除所有初始属性值")
    for player_initial_property_dict in properties_dict_list:
        property_type_cn = player_initial_property_dict['属性']
        property_type = AdditionalPropertyType.name_index_dict[property_type_cn]
        property_value = player_initial_property_dict['属性值']
        if verbose:
            print(f"初始属性名称：{property_type_cn}={property_value}")
        # 添加新的初始属性
        add_initial_properties(
            additional_property_type=property_type,
            additional_property_value=property_value,
        )


def insert_base_additional_properties(*, verbose: bool = False):
    base_property_additional_property_json_src = osp.join(local_setting.json_data_root, "properties",
                                                          'base_property_additional_properties.json')
    addition_dict_list = tools.file2dict_list(src=base_property_additional_property_json_src)
    for addition_dict in addition_dict_list:
        base_property_type_cn = addition_dict['基础属性名称']
        base_property_type = AdditionalPropertyType.name_index_dict[base_property_type_cn]

        attack_addition = addition_dict['攻击力增加']
        attack_speed_addition = addition_dict['出手速度增加']

        health_addition = addition_dict['生命值增加']
        mana_addition = addition_dict['法力值增加']

        # 先删除基础属性对应的额外属性增加值，再添加；
        del_base_additional_properties(base_property_type=base_property_type)
        if verbose:
            print(f"删除 {base_property_type_cn} 基础属性对应的额外属性值")
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
        if verbose:
            print(f"""
            基础属性名称【{base_property_type_cn}】，增加攻击力{attack_addition}，增加出手速度{attack_speed_addition}，增加生命值{health_addition}，增加法力值{mana_addition}
            """.strip())


if __name__ == '__main__':
    insert_initial_properties(verbose=local_setting.verbose)
    insert_base_additional_properties(verbose=local_setting.verbose)
