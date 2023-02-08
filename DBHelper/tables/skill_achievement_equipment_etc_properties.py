from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String,Boolean
from sqlalchemy.ext.declarative import declarative_base

from collections import defaultdict
from typing import Optional,DefaultDict


from Enums import AdditionSourceType,AdditionalPropertyType

Base = declarative_base()
from ..session import session


class SkillAchievementEquipmentEtcProperties(Base):
    """技能、装备、成就等常见的所有属性表，后期可能会更新"""
    __tablename__ = 'skill_achievement_equipment_etc_properties'

    id = Column(Integer, primary_key=True)

    additional_source_type = Column(Integer, comment="带来属性提升的物品类型，比如成就称号，技能，装备")
    additional_source_id = Column(Integer, comment="带来属性提升的物品id")

    is_temp = Column(Boolean,comment="是否为临时属性，如果是临时属性，代表是新鉴定出的属性，还没有替换当前属性。如果确定替换，则会删除临时属性。")

    physique = Column(Integer, comment='体质')
    physique_add_percent = Column(Integer, comment='体质')

    strength = Column(Integer, comment='力量')
    strength_add_percent = Column(Integer, comment='力量增加百分比')

    agility = Column(Integer, comment='敏捷')
    agility_add_percent = Column(Integer, comment='敏捷增加百分比')

    intelligence = Column(Integer, comment='智力')
    intelligence_add_percent = Column(Integer, comment='智力增加百分比')

    perception = Column(Integer, comment='感知')  #
    perception_add_percent = Column(Integer, comment='感知增加百分比')

    attack_speed = Column(Integer, comment='出手速度')
    attack_speed_add_percent = Column(Integer, comment='出手速度增加百分比')

    attack = Column(Integer, comment='攻击力')
    attack_add_percent = Column(Integer, comment='攻击力增加百分比')

    health = Column(Integer, comment='生命值')
    health_add_percent = Column(Integer, comment='生命值增加的百分比')

    health_recovery = Column(Integer, comment='生命恢复')
    health_recovery_add_percent = Column(Integer, comment='生命恢复增加百分比')

    health_absorption = Column(Integer, comment='生命吸收')
    health_absorption_add_percent = Column(Integer, comment='生命吸收')

    mana = Column(Integer, comment='法力值')
    mana_add_percent = Column(Integer, comment='法力值增加百分比')
    mana_recovery = Column(Integer, comment='法力恢复')
    mana_recovery_add_percent = Column(Integer, comment='法力恢复增加百分比')
    mana_absorption = Column(Integer, comment='法力吸收')
    mana_absorption_add_percent = Column(Integer, comment='法力吸收增加百分比')

    counterattack = Column(Integer, comment='反击值')
    counterattack_add_percent = Column(Integer, comment='反击值增加百分比')
    ignore_counterattack = Column(Integer, comment='无视反击值')
    ignore_counterattack_add_percent = Column(Integer, comment='无视反击值增加百分比')

    critical_point = Column(Integer, comment='致命点')  # 致命伤害
    critical_point_add_percent = Column(Integer, comment='致命点增加百分比')  # 致命伤害

    damage_shield = Column(Integer, comment='免伤护盾')


# 增

# 删

# 改

# 查

def get_properties_by_source_type_and_id(source_type: AdditionSourceType, source_id: int) -> Optional[SkillAchievementEquipmentEtcProperties]:
    """根据带来属性提升的物品类型和物品id查询对应的属性信息
    Args:
    session(Session): SQLAlchemy
    session对象
    source_type(int): 带来属性提升的物品类型
    source_id(int): 带来属性提升的物品id

    Returns:
    Optional[SkillAchievementEquipmentEtcProperties]: 如果找到了对应的属性信息，返回该对象，否则返回None
    """

    return session.query(SkillAchievementEquipmentEtcProperties).filter(
        SkillAchievementEquipmentEtcProperties.additional_source_type == source_type,
        SkillAchievementEquipmentEtcProperties.additional_source_id == source_id,
        SkillAchievementEquipmentEtcProperties.is_temp == False,
    ).first()

# other 
def get_properties_dict_by_source_type_and_id(source_type: AdditionSourceType, source_id: int):
    properties = get_properties_by_source_type_and_id(source_type,source_id)

    properties_dict = defaultdict(int)

    properties_dict[AdditionalPropertyType.PHYSIQUE] = properties.physique
    properties_dict[AdditionalPropertyType.PHYSIQUE_ADD_PERCENT] = properties.physique_add_percent

    properties_dict[AdditionalPropertyType.STRENGTH] = properties.strength
    properties_dict[AdditionalPropertyType.STRENGTH_ADD_PERCENT] = properties.strength_add_percent

    properties_dict[AdditionalPropertyType.AGILITY] = properties.agility
    properties_dict[AdditionalPropertyType.AGILITY_ADD_PERCENT] = properties.agility_add_percent

    properties_dict[AdditionalPropertyType.INTELLIGENCE] = properties.intelligence
    properties_dict[AdditionalPropertyType.INTELLIGENCE_ADD_PERCENT] = properties.intelligence_add_percent

    properties_dict[AdditionalPropertyType.PERCEPTION] = properties.perception
    properties_dict[AdditionalPropertyType.PERCEPTION_ADD_PERCENT] = properties.physique_add_percent

    properties_dict[AdditionalPropertyType.ATTACK_SPEED] = properties.attack_speed
    properties_dict[AdditionalPropertyType.ATTACK_SPEED_ADD_PERCENT] = properties.attack_speed_add_percent

    properties_dict[AdditionalPropertyType.ATTACK] = properties.attack
    properties_dict[AdditionalPropertyType.ATTACK_ADD_PERCENT] = properties.attack_speed_add_percent

    properties_dict[AdditionalPropertyType.HEALTH] = properties.health
    properties_dict[AdditionalPropertyType.HEALTH_ADD_PERCENT] = properties.health_add_percent

    properties_dict[AdditionalPropertyType.HEALTH_RECOVERY] = properties.health_recovery
    properties_dict[AdditionalPropertyType.HEALTH_RECOVERY_ADD_PERCENT] = properties.health_recovery_add_percent
    properties_dict[AdditionalPropertyType.HEALTH_ABSORPTION] = properties.health_absorption
    properties_dict[
        AdditionalPropertyType.HEALTH_ABSORPTION_ADD_PERCENT] = properties.health_absorption_add_percent

    properties_dict[AdditionalPropertyType.MANA] = properties.mana
    properties_dict[AdditionalPropertyType.MANA_ADD_PERCENT] = properties.mana_add_percent
    properties_dict[AdditionalPropertyType.MANA_RECOVERY] = properties.mana_recovery
    properties_dict[AdditionalPropertyType.MANA_RECOVERY_ADD_PERCENT] = properties.mana_recovery_add_percent
    properties_dict[AdditionalPropertyType.MANA_ABSORPTION] = properties.mana_absorption
    properties_dict[AdditionalPropertyType.MANA_ABSORPTION_ADD_PERCENT] = properties.mana_absorption_add_percent

    properties_dict[AdditionalPropertyType.COUNTERATTACK] = properties.counterattack
    properties_dict[AdditionalPropertyType.COUNTERATTACK_ADD_PERCENT] = properties.counterattack_add_percent
    properties_dict[AdditionalPropertyType.IGNORE_COUNTERATTACK] = properties.ignore_counterattack
    properties_dict[
        AdditionalPropertyType.IGNORE_COUNTERATTACK_ADD_PERCENT] = properties.ignore_counterattack_add_percent

    properties_dict[AdditionalPropertyType.CRITICAL_POINT] = properties.critical_point
    properties_dict[AdditionalPropertyType.CRITICAL_POINT_ADD_PERCENT] = properties.critical_point_add_percent

    properties_dict[AdditionalPropertyType.DAMAGE_SHIELD] = properties.damage_shield