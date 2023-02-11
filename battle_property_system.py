from collections import defaultdict
from typing import List

from Enums import AdditionSourceType, AdditionalPropertyType, BeingType
from DBHelper.db import *

from DBHelper.session import session

import potion_system


def add_new_player_additional_property_record(
        *,
        character_id: int,
) -> player_monster_additional_property_record.PlayerMonsterAdditionalPropertyRecord:
    """
    新增新玩家的额外属性记录，由于是新的玩家，所以所有属性都是初始值；
    :param character_id: 玩家的character_id
    :return 返回该属性的id
    """
    properties_dict = misc_properties.get_properties_dict_by_source_type(source_type=AdditionSourceType.INITIAL)

    new_additional_property_record = player_monster_additional_property_record.PlayerMonsterAdditionalPropertyRecord(
        being_type=BeingType.PLAYER,
        being_id=character_id,

        attack=properties_dict[AdditionalPropertyType.ATTACK],

        attack_speed=properties_dict[AdditionalPropertyType.ATTACK_SPEED],

        health=properties_dict[AdditionalPropertyType.HEALTH],

        health_recovery=properties_dict[AdditionalPropertyType.HEALTH_RECOVERY],

        health_absorption=properties_dict[AdditionalPropertyType.HEALTH_ABSORPTION],

        mana=properties_dict[AdditionalPropertyType.MANA],

        mana_recovery=properties_dict[AdditionalPropertyType.MANA_RECOVERY],

        mana_absorption=properties_dict[AdditionalPropertyType.MANA_ABSORPTION],

        counterattack=properties_dict[AdditionalPropertyType.COUNTERATTACK],

        ignore_counterattack=properties_dict[AdditionalPropertyType.IGNORE_COUNTERATTACK],

        critical_point=properties_dict[AdditionalPropertyType.CRITICAL_POINT],

        damage_shield=properties_dict[AdditionalPropertyType.DAMAGE_SHIELD],

        exp_add_percent=properties_dict[AdditionalPropertyType.EXP_ADD_PERCENT],
    )
    session.add(new_additional_property_record)
    session.commit()

    return new_additional_property_record


def sum_all_additional_properties(*,additional_properties_dicts: List[defaultdict[int]], ) -> defaultdict[int]:
    """
    通用函数
    :param additional_properties_dicts:  字典们，方便循环进行累加，不用写大量的键
    :return:字典类型
    """
    sum_result_dict = defaultdict(int)
    # 由于是从1开始的这样刚好包含所有的键
    for key in range(AdditionalPropertyType.min_num, AdditionalPropertyType.max_num + 1):
        sum_result_dict[key] = sum([dic[key] for dic in additional_properties_dicts])
    return sum_result_dict


def get_equipment_improved_properties(*,equipment_additional_properties_dict: defaultdict[int], improve_rate: float):
    """
    获取经过百分比提升之后的属性效果（目前只有装备升星这个途径；）
    :param equipment_additional_properties_dict:
    :param improve_rate:    浮点类型，如果是0.1，则最终加成为1.1。
    :return:
    """
    for key in equipment_additional_properties_dict:
        equipment_additional_properties_dict[key] = int(
            equipment_additional_properties_dict[key] * (1 + improve_rate)  # 此处int期望为向下取整
        )
    return equipment_additional_properties_dict


def get_player_achievement_title_additional_properties_dict_by_character_id(*,character_id: int):
    """
    获取所有属性。玩家->成就对应的称号->属性
    :param character_id:
    :return:
    """
    record = player_achievement_record.get_player_achievement_title_by_character_id(character_id)

    achievement_properties_dict = misc_properties.get_properties_dict_by_source_type_and_source_id(
        source_type=AdditionSourceType.ACHIEVEMENT,
        source_id=record.achievement_id
    )
    return achievement_properties_dict


def get_player_potion_additional_properties_dict(*,character_id: int):
    """
    获取所有属性。玩家->临时药剂->临时属性
    :param character_id:
    :return:
    """

    potion_record = potion_system.get_player_unexpired_potion_record_by_record_id(character_id=character_id)

    potion_properties_dict = misc_properties.get_properties_dict_by_source_type_and_source_id(
        source_type=AdditionSourceType.POTION,
        source_id=potion_record.potion_id
    )
    return potion_properties_dict


def get_all_player_base_properties_dict_by_character_id(*, character_id: int) -> dict:
    """
    玩家->基础属性->属性
    获取所有基础属性加点带来的属性提升
    :param character_id:
    :return:
    """
    all_player_base_properties_dict = misc_properties.get_properties_dict_by_source_type_and_source_id(
        source_type=AdditionSourceType.BASE_PROPERTY_POINT,  # 基础属性加点
        source_id=character_id,
    )
    return all_player_base_properties_dict


def get_all_initial_properties_dict() -> dict:
    """
     ->初始属性（每个玩家都一样,所以不需要任何）
    :return:
    """
    all_player_initial_properties_dict = misc_properties.get_properties_dict_by_source_type(
        source_type=AdditionSourceType.INITIAL,  # 基础属性加点
    )
    return all_player_initial_properties_dict


def get_all_player_initial_additional_property(*,character_id: int):
    """
    获取所有属性
    :param character_id:
    :return:
    """
    dicts = []

    all_player_achievement_records = player_achievement_record.get_all_achievements_records_by_character_id(
        character_id)
    for record in all_player_achievement_records:
        achievement_properties_dict = misc_properties.get_properties_dict_by_source_type_and_source_id(
            source_type=AdditionSourceType.ACHIEVEMENT,
            source_id=record.achievement_id)
        dicts.append(achievement_properties_dict)

    all_achievements_addition_properties_dict = sum_all_additional_properties(
        dicts,
    )

    return all_achievements_addition_properties_dict


def get_all_skills_additional_properties_by_character_id(*,character_id: int):
    """
    根据人物id查询所有技能的附加属性
    :param character_id:
    :return:
    """
    dicts = []

    skills = player_skill_record.get_player_all_skill_record_by_character_id(character_id)
    for one_skill in skills:
        one_skill_book = skill_book.get_skill_book_by_skill_id_skill_level(one_skill.id, one_skill.skill_level)

        skill_additional_properties_dict = misc_properties.get_properties_dict_by_source_type_and_source_id(
            source_type=AdditionSourceType.SKILL,
            source_id=one_skill_book.id)
        dicts.append(skill_additional_properties_dict)

    result_properties_dict = sum_all_additional_properties(dicts)
    return result_properties_dict


def get_all_equipments_additional_properties_by_character_id(*,character_id: int):
    """
    根据人物id查询所有装备的附加属性。并且计算装备上的宝石、升星。
    :param character_id:
    :return:
    """
    dicts = []

    equipments = player_stuff_record.get_all_wearing_stuffs_by_character_id(character_id)
    for equipment in equipments:

        # 获取装备升星带来的属性提升
        equipment_additional_properties_dict = misc_properties.get_properties_dict_by_source_type_and_source_id(
            source_type=AdditionSourceType.EQUIPMENT,
            source_id=equipment.id)
        cur_star_improve_rate = (equipment.current_stars_num * setting.get_per_star_improved_percent()) / 100
        equipment_properties_dict = get_equipment_improved_properties(
            equipment_additional_properties_dict=equipment_additional_properties_dict,
            improve_rate=cur_star_improve_rate
        )
        dicts.append(equipment_properties_dict)

        # 获取装备宝石带来的属性提升；
        gems_properties_dict = []
        equipment_gems = equipment_gem_record.get_all_gems_by_equipment_id(equipment.id)
        for equipment_gem in equipment_gems:  # 一个装备有若干个宝石
            one_gem = equipment_gem.gem_idget_gem_by_gem_id(equipment_gem.gem_id)
            gems_properties_dict[one_gem.base_property_type] += one_gem.increase
        dicts.append(gems_properties_dict)

    # 计算所有属性加成
    result_properties_dict = sum_all_additional_properties(dicts)
    return result_properties_dict


def get_player_initial_skills_achievements_equipments_properties_dict(*,character_id: int):
    """
    获取人物初始、技能、成就称号、装备所获得的所有属性
    :param character_id:
    :return:
    """
    additional_properties = defaultdict(int)

    # 初始属性。每个玩家都一样，所以不需要任何参数就可以查询到；
    initial_additional_properties = get_all_initial_properties_dict()
    # 玩家->基础属性加点->属性提升
    base_property_point_properties_dict = get_all_player_base_properties_dict_by_character_id(character_id=character_id)
    # 玩家->技能->属性提升
    skill_properties_dict = get_all_skills_additional_properties_by_character_id(character_id=character_id)
    # 玩家->成就称号->属性提升
    achievement_properties_dict = get_player_achievement_title_additional_properties_dict_by_character_id(
        character_id=character_id)
    # 玩家->装备+升星+镶嵌宝石->属性提升
    equipment_properties_dict = get_all_equipments_additional_properties_by_character_id(character_id=character_id)
    # 玩家->药剂->临时属性提升
    potion_properties_dict = get_player_potion_additional_properties_dict(character_id=character_id)

    for dic in [initial_additional_properties,
                base_property_point_properties_dict,
                skill_properties_dict,
                achievement_properties_dict,
                equipment_properties_dict,
                potion_properties_dict]:

        for key in range(AdditionalPropertyType.min_num, AdditionalPropertyType.max_num + 1):
            additional_properties[key] += dic[key]

    return additional_properties


if __name__ == '__main__':
    get_player_initial_skills_achievements_equipments_properties_dict(1)
