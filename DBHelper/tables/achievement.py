import inspect
from typing import List

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session
from Enums import AchievementType, AdditionalPropertyType
from DBHelper.tables.base_table import Entity

Base = declarative_base()

"""
如果是第一次进入游戏，达成条件对应的属性为空。属性值为空。
如果是基础属性突破，则属性和值均可填写。
如果是等级相关，则对应属性为空，属性值为等级；
如果是击杀boss相关，则对应属性为空，属性值为击杀数量。击杀数量通过击杀表来体现；
如果是FIRST_PK，则对应属性为空，属性值为空；
如果是PK_RANK，则对应属性为空，属性值为排名；
如果是GOLD_NUM_INCREASE，则对应属性为空，属性值为黄金数量；
如果是FIRST_SKILL，则对应属性类型为空，属性值为空。
如果是SKILL，则对应属性类型为空，属性值为技能数；
如果是FULL_SKILL，则对应属性类型为空，属性值为满9的个数；
如果是FIRST_LOTTERY,则对应属性类型为空，属性值为空。初次抽奖触发
如果是LOTTERY，则对应属性类型为空，属性值为中奖次数
如果是FULL_EQUIPMENT，则对应属性类型为空，属性值为穿戴装备数量；
如果是EQUIPMENT，则对应属性类型为品质id，属性值为数量。含义为，穿戴装备均在某个品质及以上；
如果是FIRST_SELL_STUFF，则对应属性为空，属性值为空。
如果是FIRST_EXP_BOOK,则对应属性为类型为空，属性值为空。
如果是FIRST_IDENTIFY,则对应属性为类型空，属性值为空。
如果是FIRST_RAISE_STAR，则对应属性类型为空，属性值为空。
如果是RAISE_STAR，则对应属性类型为空，属性值为所穿戴装备中最高的升星数量。
如果是ALL_RAISE_STAR，则对应属性类型为空，属性值为所有穿戴装备升星数量。
"""


# 成就系统
class Achievement(Entity):
    """
    有哪些成就可以达成
    """
    __tablename__ = "achievement"

    achievement_type = Column(Integer, comment="成就类型")

    condition_property_type = Column(Integer, comment="达成条件对应的属性")
    condition_property_value = Column(Integer, comment="达成条件对应属性应该达到的值。")

    achievement_point = Column(Integer, comment="根据达成难度获得成就点数")

    days_of_validity = Column(Integer, comment="有效期。以天为单位。如果是-1则代表是永久。")
    introduce = Column(String, comment="对于成就的介绍")

    @classmethod
    def add_or_update_by_name(cls,
                              *,
                              name: str,

                              achievement_type: int = None,

                              condition_property_type: int = None,
                              condition_property_value: int = None,

                              achievement_point: int = None,

                              days_of_validity: int = None,
                              introduce: str = None,
                              ) -> "Achievement":

        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_name)
        record = cls._add_or_update_by_name(**fields)
        return record

    # 改
    @classmethod
    def add_or_update_by_id(
            cls,
            *,
            _id: int,

            name: str = None,
            achievement_type: AchievementType = None,
            condition_type: int = None,
            condition_value: int = None,
            days_of_validity: int = None,
            achievement_point: int = None,
            introduce: str = None,
    ) -> "Achievement":

        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
        return record
