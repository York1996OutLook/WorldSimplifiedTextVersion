from typing import List, Optional, DefaultDict

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from Enums import BeingType, AdditionalPropertyType

from DBHelper.session import session

Base = declarative_base()


class PlayerMonsterAdditionalPropertyRecord(Base):
    """人物、怪物常见的所有属性表，后期可能会更新。这个表中的数据依赖于其它的表格；"""
    __tablename__ = 'player_monster_additional_property_record'

    id = Column(Integer, primary_key=True)

    being_type = Column(Integer, comment="生物类型，参考枚举类型；目前是人物或者boss")
    being_id = Column(Integer, comment="生物ID，根据不同的being_type去查询不同的表格")

    additional_property_type = Column(Integer, comment="附加属性的类型")
    additional_property_value = Column(Integer, comment="附加属性的值")

    def __init__(self, *,
                 being_type: int,
                 being_id: int = None,
                 additional_property_type: int = None,
                 additional_property_value: int = None,
                 ):
        self.being_type = being_type
        self.being_id = being_id
        self.additional_property_type = additional_property_type
        self.additional_property_value = additional_property_value


# 增
def add(
        *,
        being_type: BeingType,
        being_id: int,
        attack_speed: int,
        attack: int,
        health: int,
        health_recovery: int,
        health_absorption: int,
        mana: int,
        mana_recovery: int,
        mana_absorption: int,
        counterattack: int,
        ignore_counterattack: int,
        critical_point: int,
        damage_shield: int,
        exp_add_percent: int,
):
    """
    新增人物、怪物常见属性记录
    :param being_type: 出手速度
    :param being_id: 出手速度
    :param attack_speed: 出手速度
    :param attack: 攻击力
    :param health: 生命值
    :param health_recovery: 生命恢复
    :param health_absorption: 生命吸收
    :param mana: 法力值
    :param mana_recovery: 法力恢复
    :param mana_absorption: 法力吸收
    :param counterattack: 反击值
    :param ignore_counterattack: 无视反击值
    :param critical_point: 致命点
    :param damage_shield: 免伤护盾
    :param exp_add_percent: 经验值加成

    :return 返回该属性的id
    """
    # 随机生成成就记录
    achievement_list = [{"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.PHYSIQUE,
                         "additional_property_value": 0},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.PHYSIQUE_ADD_PERCENT,
                         "additional_property_value": 0},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.STRENGTH,
                         "additional_property_value": 0},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.STRENGTH_ADD_PERCENT,
                         "additional_property_value": 0},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.AGILITY,
                         "additional_property_value": 0},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.AGILITY_ADD_PERCENT,
                         "additional_property_value": 0},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.INTELLIGENCE,
                         "additional_property_value": 0},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.INTELLIGENCE_ADD_PERCENT,
                         "additional_property_value": 0},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.PERCEPTION,
                         "additional_property_value": 0},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.PERCEPTION_ADD_PERCENT,
                         "additional_property_value": 0},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.ATTACK_SPEED,
                         "additional_property_value": attack_speed},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.ATTACK_SPEED_ADD_PERCENT,
                         "additional_property_value": 0},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.ATTACK,
                         "additional_property_value": attack},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.ATTACK_ADD_PERCENT,
                         "additional_property_value": 0},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.HEALTH,
                         "additional_property_value": health},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.HEALTH_ADD_PERCENT,
                         "additional_property_value": 0},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.HEALTH_RECOVERY,
                         "additional_property_value": health_recovery},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.HEALTH_RECOVERY_ADD_PERCENT,
                         "additional_property_value": 0},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.HEALTH_ABSORPTION,
                         "additional_property_value": health_absorption},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.HEALTH_ABSORPTION_ADD_PERCENT,
                         "additional_property_value": 0},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.MANA,
                         "additional_property_value": mana},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.MANA_ADD_PERCENT,
                         "additional_property_value": 0},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.MANA_RECOVERY,
                         "additional_property_value": mana_recovery},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.MANA_RECOVERY_ADD_PERCENT,
                         "additional_property_value": 0},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.MANA_ABSORPTION,
                         "additional_property_value": mana_absorption},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.MANA_ABSORPTION_ADD_PERCENT,
                         "additional_property_value": 0},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.COUNTERATTACK,
                         "additional_property_value": counterattack},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.COUNTERATTACK_ADD_PERCENT,
                         "additional_property_value": 0},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.IGNORE_COUNTERATTACK,
                         "additional_property_value": ignore_counterattack},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.IGNORE_COUNTERATTACK_ADD_PERCENT,
                         "additional_property_value": 0},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.CRITICAL_POINT,
                         "additional_property_value": critical_point},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.CRITICAL_POINT_ADD_PERCENT,
                         "additional_property_value": 0},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.DAMAGE_SHIELD,
                         "additional_property_value": damage_shield},

                        {"being_type": being_type,
                         "being_id": being_id,
                         "additional_property_type": AdditionalPropertyType.EXP_ADD_PERCENT,
                         "additional_property_value": exp_add_percent},
                        ]

    # 插入数据
    for one_record in achievement_list:
        new_record = PlayerMonsterAdditionalPropertyRecord(
            being_type=one_record["being_type"],
            being_id=one_record["being_id"],
            additional_property_type=one_record["additional_property_type"],
            additional_property_value=one_record["additional_property_value"]
        )
        session.add(new_record)
    session.commit()


# 删
def delete_by_record_id(*, record_id: int) -> None:
    """
    删除人物额外属性记录
    :param record_id: 记录ID
    :return: None
    """
    session.query(PlayerMonsterAdditionalPropertyRecord).filter(
        PlayerMonsterAdditionalPropertyRecord.id == record_id).delete()
    session.commit()


# 改


def update_by_being_and_properties_dict(
        *,
        being_type: int,
        being_id: int,
        properties_dict: DefaultDict[int, int],
):
    """
    更新附加属性记录

    :param being_type: 生物类型：玩家或者boss
    :param being_id: 玩家id或者生物id
    :param properties_dict: 额外属性表
    :return: None
    """
    for additional_property_type in properties_dict:
        record = session.query(PlayerMonsterAdditionalPropertyRecord).filter_by(
            being_type=being_type,
            being_id=being_id,
            additional_property_type=additional_property_type,
        ).first()
        record.additional_property_value = properties_dict[additional_property_type]

    session.commit()


# 查
def get_by_record_id(*, record_id: int) -> Optional[PlayerMonsterAdditionalPropertyRecord]:
    """
    获取人物或者怪物额外属性记录
    :param record_id: 记录ID
    :return: 人物额外属性记录对象，若不存在则返回None
    """
    return session.query(PlayerMonsterAdditionalPropertyRecord).filter(
        PlayerMonsterAdditionalPropertyRecord.id == record_id).first()


