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


# 增

# 删

# 改

# 查
def get_potion_by_potion_id(*,
                            potion_id: int
                            ) -> Potion:
    """
    根据potion的id查询你potion
    """
    potion = session.query(Potion).filter(Potion.id == potion_id)
    return potion


if __name__ == '__main__':
    potions = [
        Potion(name="体质药水",
               additional_property_type=AdditionalPropertyType.PHYSIQUE,
               additional_property_value=30,
               duration_by_min=10,
               is_bind=False,
               ),
        Potion(name="强效体质药水",
               additional_property_type=AdditionalPropertyType.PHYSIQUE,
               additional_property_value=100,
               duration_by_min=10,
               is_bind=False,
               ),

        Potion(name="力量药水",
               additional_property_type=AdditionalPropertyType.STRENGTH,
               additional_property_value=30,
               duration_by_min=10,
               is_bind=False,
               ),
        Potion(name="强效力量药水",
               additional_property_type=AdditionalPropertyType.STRENGTH,
               additional_property_value=100,
               duration_by_min=10,
               is_bind=False,
               ),

        Potion(name="敏捷药水",
               additional_property_type=AdditionalPropertyType.AGILITY,
               additional_property_value=30,
               duration_by_min=10,
               is_bind=False,
               ),
        Potion(name="强效敏捷药水",
               additional_property_type=AdditionalPropertyType.AGILITY,
               additional_property_value=100,
               duration_by_min=10,
               is_bind=False,
               ),

        Potion(name="智力药水",
               additional_property_type=AdditionalPropertyType.INTELLIGENCE,
               additional_property_value=30,
               duration_by_min=10,
               is_bind=False,
               ),
        Potion(name="强效智力药水",
               additional_property_type=AdditionalPropertyType.INTELLIGENCE,
               additional_property_value=100,
               duration_by_min=10,
               is_bind=False,
               ),

        Potion(name="感知药水",
               additional_property_type=AdditionalPropertyType.PERCEPTION,
               additional_property_value=30,
               duration_by_min=10,
               is_bind=False,
               ),
        Potion(name="强效感知药水",
               additional_property_type=AdditionalPropertyType.PERCEPTION,
               additional_property_value=100,
               duration_by_min=10,
               is_bind=False,
               ),

        Potion(name="攻击力药水",
               additional_property_type=AdditionalPropertyType.ATTACK,
               additional_property_value=1000,
               duration_by_min=10,
               is_bind=False,
               ),
        Potion(name="强效攻击力药水",
               additional_property_type=AdditionalPropertyType.ATTACK,
               additional_property_value=5000,
               duration_by_min=10,
               is_bind=False,
               ),

        Potion(name="出手速度药水",
               additional_property_type=AdditionalPropertyType.ATTACK_SPEED,
               additional_property_value=1000,
               duration_by_min=10,
               is_bind=False,
               ),
        Potion(name="强效出手速度药水",
               additional_property_type=AdditionalPropertyType.ATTACK_SPEED,
               additional_property_value=5000,
               duration_by_min=10,
               is_bind=False,
               ),

        Potion(name="生命药水",
               additional_property_type=AdditionalPropertyType.HEALTH,
               additional_property_value=1000,
               duration_by_min=10,
               is_bind=False,
               ),
        Potion(name="强效生命药水",
               additional_property_type=AdditionalPropertyType.HEALTH,
               additional_property_value=5000,
               duration_by_min=10,
               is_bind=False,
               ),

        Potion(name="法力药水",
               additional_property_type=AdditionalPropertyType.MANA,
               additional_property_value=1000,
               duration_by_min=10,
               is_bind=False,
               ),
        Potion(name="强效法力药水",
               additional_property_type=AdditionalPropertyType.MANA,
               additional_property_value=5000,
               duration_by_min=10,
               is_bind=False,
               ),

        Potion(name="反击药水",
               additional_property_type=AdditionalPropertyType.COUNTERATTACK,
               additional_property_value=100,
               duration_by_min=10,
               is_bind=False,
               ),
        Potion(name="强效反击药水",
               additional_property_type=AdditionalPropertyType.COUNTERATTACK,
               additional_property_value=1000,
               duration_by_min=10,
               is_bind=False,
               ),

        Potion(name="致命药水",
               additional_property_type=AdditionalPropertyType.CRITICAL_POINT,
               additional_property_value=100,
               duration_by_min=10,
               is_bind=False,
               ),
        Potion(name="强效致命药水",
               additional_property_type=AdditionalPropertyType.CRITICAL_POINT,
               additional_property_value=1000,
               duration_by_min=10,
               is_bind=False,
               ),

        Potion(name="免伤护盾药水",
               additional_property_type=AdditionalPropertyType.DAMAGE_SHIELD,
               additional_property_value=1,
               duration_by_min=10,
               is_bind=False,
               ),
        Potion(name="强效免伤护盾药水",
               additional_property_type=AdditionalPropertyType.DAMAGE_SHIELD,
               additional_property_value=2,
               duration_by_min=10,
               is_bind=False,
               ),

        Potion(name="经验加成药水",
               additional_property_type=AdditionalPropertyType.EXP_ADD_PERCENT,
               additional_property_value=10,
               duration_by_min=10,
               is_bind=False,
               ),
        Potion(name="强效经验加成药水",
               additional_property_type=AdditionalPropertyType.EXP_ADD_PERCENT,
               additional_property_value=30,
               duration_by_min=10,
               is_bind=False,
               ),
    ]
    session.add_all(potions)
    session.commit()
