from typing import List

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session
from Enums import AdditionalPropertyType

Base = declarative_base()


# 药剂系统
class Potion(Base):
    """
    药剂
    """
    __tablename__ = "potion"

    id = Column(Integer, primary_key=True, comment="药剂ID")
    name = Column(String, comment="药剂名称")

    additional_property_type = Column(Integer, comment="附加属性的类型，参考AdditionalPropertyType")
    additional_property_value = Column(Integer, comment="附加属性的值")

    duration_by_min = Column(Integer, comment="有效期，以分钟为单位")

    is_bind = Column(Boolean, comment="刚出来的时候是否已经绑定")

    def __init__(self,
                 *,
                 name: str,
                 additional_property_type: AdditionalPropertyType,
                 additional_property_value: int,
                 duration_by_min: int,
                 is_bind: bool):
        self.name = name
        self.additional_property_type = additional_property_type
        self.additional_property_value = additional_property_value
        self.duration_by_min = duration_by_min
        self.is_bind = is_bind


# 增
def add(*,
               name: str,
               additional_property_type: AdditionalPropertyType,
               additional_property_value: int,
               duration_by_min: int,
               is_bind: bool,
               ) -> Potion:
    """

    :param name:
    :param additional_property_type:
    :param additional_property_value:
    :param duration_by_min:
    :param is_bind:
    :return:
    """
    potion = Potion(name=name, additional_property_type=additional_property_type,
                    additional_property_value=additional_property_value, duration_by_min=duration_by_min,
                    is_bind=is_bind)
    session.add(potion)
    session.commit()
    return potion


def add_or_update_by_name(*,
                                 name: str,
                                 additional_property_type: AdditionalPropertyType,
                                 additional_property_value: int,
                                 duration_by_min: int,
                                 is_bind: bool,
                                 ) -> Potion:
    if is_exists_by_name(name=name):
        potion = update_potion_by_name(
            name=name,
            additional_property_type=additional_property_type,
            additional_property_value=additional_property_value,
            duration_by_min=duration_by_min,
            is_bind=is_bind
        )
    else:
        potion = add(name=name,
                            additional_property_type=additional_property_type,
                            additional_property_value=additional_property_value,
                            duration_by_min=duration_by_min,
                            is_bind=is_bind
                            )
    return potion


# 删

# 改
def update_by_name(*,
                          name: str,
                          additional_property_type: AdditionalPropertyType = None,
                          additional_property_value: int = None,
                          duration_by_min: int = None,
                          is_bind: bool = None, ) -> Potion:
    potion = session.query(Potion).filter(Potion.name == name).first()
    if additional_property_type is not None:
        potion.additional_property_type = additional_property_type
    if additional_property_value is not None:
        potion.additional_property_value = additional_property_value
    if duration_by_min is not None:
        potion.duration_by_min = duration_by_min
    if is_bind is not None:
        potion.is_bind = is_bind

    session.commit()
    return potion


# 查

def get_by_potion_id(*,
                            potion_id: int
                            ) -> Potion:
    """
    根据potion的id查询你potion
    """
    potion = session.query(Potion).filter(Potion.id == potion_id).first()
    return potion


def is_exists_by_name(*, name: str):
    """
    根据name判断是否存在
    :param name:
    :return:
    """
    potion = session.query(Potion).filter(Potion.name == name).first()
    return potion is not None


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
        add_or_update_potion_by_name(name=one_potion['name'],
                                     additional_property_type=one_potion['additional_property_type'],
                                     additional_property_value=one_potion['additional_property_value'],
                                     duration_by_min=one_potion['duration_by_min'],
                                     is_bind=one_potion['is_bind'],
                                     )
