from typing import List

from sqlalchemy import Integer, String, Boolean,Text
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session
from Enums import AdditionalPropertyType,DurationByHours
from DBHelper.tables.base_table import Entity
from DBHelper.tables.base_table import CustomColumn

Base = declarative_base()


# 药剂系统
class Potion(Entity,Base):
    """
    药剂
    """
    __cn__ = "药剂"

    __tablename__ = "potion"
    id = CustomColumn(Integer, cn="ID", primary_key=True, editable=False,autoincrement=True)

    name = CustomColumn(Text, cn='名称')  # 显式复制并设置 cn 属性

    duration_by_hour = CustomColumn(Integer,cn='有效期/小时',bind_type=DurationByHours, comment="有效期,以小时为单位")
    is_bind = CustomColumn(Boolean,cn='是否绑定', comment="刚出来的时候是否已经绑定")

    @classmethod
    def add_or_update_by_name(cls,
                              *,
                              name: str,
                              duration_by_min: int = None,
                              is_bind: bool = None
                              ) -> "Potion":
        record = cls._add_or_update_by_name(kwargs=locals())
        return record

    @classmethod
    def add_or_update_by_id(
            cls,
            *,
            _id: int,

            name: str = None,
            duration_by_min: int = None,
            is_bind: bool = None
    ) -> "Potion":
        record = cls._add_or_update_by_id(kwargs=locals())
        return record


if __name__ == '__main__':
    potions = [
        {"name": "体质药水",
         "additional_property_type": AdditionalPropertyType.PHYSIQUE,
         "additional_property_value": 30,
         "duration_by_min": 10,
         "is_bind": False,
         },
        {"name": "强效体质药水",
         "additional_property_type": AdditionalPropertyType.PHYSIQUE,
         "additional_property_value": 100,
         "duration_by_min": 10,
         "is_bind": False,
         },

        {"name": "力量药水",
         "additional_property_type": AdditionalPropertyType.STRENGTH,
         "additional_property_value": 30,
         "duration_by_min": 10,
         "is_bind": False,
         },
        {"name": "强效力量药水",
         "additional_property_type": AdditionalPropertyType.STRENGTH,
         "additional_property_value": 100,
         "duration_by_min": 10,
         "is_bind": False,
         },

        {"name": "敏捷药水",
         "additional_property_type": AdditionalPropertyType.AGILITY,
         "additional_property_value": 30,
         "duration_by_min": 10,
         "is_bind": False,
         },
        {"name": "强效敏捷药水",
         "additional_property_type": AdditionalPropertyType.AGILITY,
         "additional_property_value": 100,
         "duration_by_min": 10,
         "is_bind": False,
         },

        {"name": "智力药水",
         "additional_property_type": AdditionalPropertyType.INTELLIGENCE,
         "additional_property_value": 30,
         "duration_by_min": 10,
         "is_bind": False,
         },
        {"name": "强效智力药水",
         "additional_property_type": AdditionalPropertyType.INTELLIGENCE,
         "additional_property_value": 100,
         "duration_by_min": 10,
         "is_bind": False,
         },

        {"name": "感知药水",
         "additional_property_type": AdditionalPropertyType.PERCEPTION,
         "additional_property_value": 30,
         "duration_by_min": 10,
         "is_bind": False,
         },
        {"name": "强效感知药水",
         "additional_property_type": AdditionalPropertyType.PERCEPTION,
         "additional_property_value": 100,
         "duration_by_min": 10,
         "is_bind": False,
         },

        {"name": "攻击力药水",
         "additional_property_type": AdditionalPropertyType.ATTACK,
         "additional_property_value": 1000,
         "duration_by_min": 10,
         "is_bind": False,
         },
        {"name": "强效攻击力药水",
         "additional_property_type": AdditionalPropertyType.ATTACK,
         "additional_property_value": 5000,
         "duration_by_min": 10,
         "is_bind": False,
         },

        {"name": "出手速度药水",
         "additional_property_type": AdditionalPropertyType.ATTACK_SPEED,
         "additional_property_value": 1000,
         "duration_by_min": 10,
         "is_bind": False,
         },
        {"name": "强效出手速度药水",
         "additional_property_type": AdditionalPropertyType.ATTACK_SPEED,
         "additional_property_value": 5000,
         "duration_by_min": 10,
         "is_bind": False,
         },

        {"name": "生命药水",
         "additional_property_type": AdditionalPropertyType.HEALTH,
         "additional_property_value": 1000,
         "duration_by_min": 10,
         "is_bind": False,
         },
        {"name": "强效生命药水",
         "additional_property_type": AdditionalPropertyType.HEALTH,
         "additional_property_value": 5000,
         "duration_by_min": 10,
         "is_bind": False,
         },

        {"name": "法力药水",
         "additional_property_type": AdditionalPropertyType.MANA,
         "additional_property_value": 1000,
         "duration_by_min": 10,
         "is_bind": False,
         },
        {"name": "强效法力药水",
         "additional_property_type": AdditionalPropertyType.MANA,
         "additional_property_value": 5000,
         "duration_by_min": 10,
         "is_bind": False,
         },

        {"name": "反击药水",
         "additional_property_type": AdditionalPropertyType.COUNTERATTACK,
         "additional_property_value": 100,
         "duration_by_min": 10,
         "is_bind": False,
         },
        {"name": "强效反击药水",
         "additional_property_type": AdditionalPropertyType.COUNTERATTACK,
         "additional_property_value": 1000,
         "duration_by_min": 10,
         "is_bind": False,
         },

        {"name": "致命药水",
         "additional_property_type": AdditionalPropertyType.CRITICAL_POINT,
         "additional_property_value": 100,
         "duration_by_min": 10,
         "is_bind": False,
         },
        {"name": "强效致命药水",
         "additional_property_type": AdditionalPropertyType.CRITICAL_POINT,
         "additional_property_value": 1000,
         "duration_by_min": 10,
         "is_bind": False,
         },

        {"name": "免伤护盾药水",
         "additional_property_type": AdditionalPropertyType.DAMAGE_SHIELD,
         "additional_property_value": 1,
         "duration_by_min": 10,
         "is_bind": False,
         },
        {"name": "强效免伤护盾药水",
         "additional_property_type": AdditionalPropertyType.DAMAGE_SHIELD,
         "additional_property_value": 2,
         "duration_by_min": 10,
         "is_bind": False,
         },

        {"name": "经验加成药水",
         "additional_property_type": AdditionalPropertyType.EXP_ADD_PERCENT,
         "additional_property_value": 10,
         "duration_by_min": 10,
         "is_bind": False,
         },
        {"name": "强效经验加成药水",
         "additional_property_type": AdditionalPropertyType.EXP_ADD_PERCENT,
         "additional_property_value": 30,
         "duration_by_min": 10,
         "is_bind": False,
         },
    ]
    for one_potion in potions:
        add_or_update_by_name(name=one_potion['name'],
                              additional_property_type=one_potion['additional_property_type'],
                              additional_property_value=one_potion['additional_property_value'],
                              duration_by_min=one_potion['duration_by_min'],
                              is_bind=one_potion['is_bind'],
                              )
