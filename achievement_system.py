from typing import List

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.db import *
from DBHelper.session import session
from Enums import AchievementType, AdditionalPropertyType, StuffType, AdditionSourceType, EquipmentPropertyAvailability

Base = declarative_base()

if __name__ == '__main__':
    achievement_list = [
        {
            # base
            "name": "初入世界",
            "achievement_type": AchievementType.ENTER_THE_GAME,
            "condition": "第一次进入世界ol",
            "introduce": """
柔情侠骨，血雨腥风。你行走在黑暗中，那些疯狂的恶徒不断地纠缠着你。你冷静地抽出了你锋利的刀，准备为了正义而战。你知道这是一场永无止境的战斗，因为总有更多的邪恶存在于这个世界上，你将继续前行，永不停歇，为了黎民苍生，为了正义。""",

            # additional_properties
            'additional_properties': [
                {
                    "additional_property_type": AdditionalPropertyType.ATTACK,
                    "additional_property_value": 10,
                }
            ]
        },
    ]

    for achievement_dict in achievement_list:
        # 如果某个称号的名字已经存在，则跳过；
        if achievement.is_achievement_exists_by_name(name=achievement_dict['name']):
            one_achievement = achievement.get_achievement_by_achievement_name(name=achievement_dict['name'])

            achievement.update_achievement(achievement_id=one_achievement.id,
                                           new_achievement_type=achievement_dict['achievement_type'],
                                           new_name=achievement_dict['name'],
                                           new_condition=achievement_dict['condition'],
                                           new_introduce=achievement_dict['introduce']
                                           )
            for property_index, additional_property in enumerate(achievement_dict['additional_properties']):
                # 不管是否存在，执行删除操作语句
                misc_properties.del_achievement_properties(
                    achievement_id=one_achievement.id,
                )
        else:
            # 添加新的成就
            one_achievement = achievement.Achievement(
                name=achievement_dict["name"],
                achievement_type=achievement_dict["achievement_type"],
                condition=achievement_dict["condition"],
                introduce=achievement_dict["introduce"]
            )
            session.add(one_achievement)

        # 添加成就对应的属性加成
        for property_index, additional_property in enumerate(achievement_dict['additional_properties']):
            properties_record = misc_properties.InitialSkillAchievementEquipmentPotionEtcPropertiesRecord(
                additional_source_type=AdditionSourceType.ACHIEVEMENT,
                additional_source_id=one_achievement.id,
                additional_source_property_index=property_index,
                additional_property_type=additional_property['additional_property_type'],
                additional_property_value=additional_property['additional_property_value'],
            )
            session.add(properties_record)
    session.commit()
