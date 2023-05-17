import inspect
from typing import List

from sqlalchemy import Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session
from Enums import AchievementType, AdditionalPropertyType, AchievementPropertyType, BindType
from DBHelper.tables.base_table import Entity
from DBHelper.tables.base_table import CustomColumn

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
class Achievement(Entity, Base):

    __cn__ = "成就"

    __tablename__ = "achievement"

    id = CustomColumn(Integer, cn="ID", primary_key=True)
    name = CustomColumn(Text, cn='名称')  # 显式复制并设置 cn 属性

    achievement_type = CustomColumn(Integer, cn="成就类型", bind_type=AchievementType,comment="成就类型")

    condition_property_type = CustomColumn(Integer, cn="条件类型", bind_type=AchievementPropertyType,comment="达成条件对应的属性")
    condition_property_value = CustomColumn(Integer, cn="条件值", comment="达成条件对应属性应该达到的值。")

    achievement_point = CustomColumn(Integer, cn="成就点", comment="根据达成难度获得成就点数")

    days_of_validity = CustomColumn(Integer, cn="有效期/天", comment="有效期。以天为单位。如果是-1则代表是永久。")
    introduce = CustomColumn(Text, cn="介绍", comment="对于成就的介绍")

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
        record = cls._add_or_update_by_name(kwargs=locals())
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
        """
        根据id进行查询，然后更新其他的参数
        """
        record = cls._add_or_update_by_id(kwargs=locals())
        return record
