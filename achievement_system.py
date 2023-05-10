from typing import List

from sqlalchemy import Integer, String
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.db import *
from DBHelper.session import session
from Enums import AchievementType, AdditionalPropertyType, StuffType, AdditionSourceType, PropertyAvailability
from DBHelper.tables.base_table import CustomColumn

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
        # 如果存在则更新，不存在则新建
        one_achievement = achievement.add_or_update_achievement(
            name=achievement_dict['name'],
            achievement_type=achievement_dict['achievement_type'],
            condition=achievement_dict['condition'],
            introduce=achievement_dict['introduce'],
        )

        # 删除原有成就对应的属性
        misc_properties.del_achievement_properties(
            achievement_id=one_achievement.id,
        )

        # 添加成就对应的属性加成。一个成就可能有多条属性加成；
        for property_index, additional_property in enumerate(achievement_dict['additional_properties']):
            misc_properties.add_achievement_properties(
                achievement_id=one_achievement.id,
                additional_source_property_index=property_index,
                additional_property_type=additional_property['additional_property_type'],
                additional_property_value=additional_property['additional_property_value'],
            )
