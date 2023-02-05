from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Optional

Base = declarative_base()

# 创建数据库连接引擎
engine = create_engine('sqlite:///example.db')

# 创建会话
Session = sessionmaker(bind=engine)
session = Session()


class AdditionalPropertyRecord(Base):
    """人物、怪物常见的所有属性表，后期可能会更新"""
    __tablename__ = 'additional_property_record'

    id = Column(Integer, primary_key=True)

    attack_speed = Column(Integer, comment='出手速度')

    attack = Column(Integer, comment='攻击力')

    health = Column(Integer, comment='生命值')
    health_recovery = Column(Integer, comment='生命恢复')
    health_absorption = Column(Integer, comment='生命吸收')

    mana = Column(Integer, comment='法力值')
    mana_recovery = Column(Integer, comment='法力恢复')
    mana_absorption = Column(Integer, comment='法力吸收')

    counterattack = Column(Integer, comment='反击值')
    ignore_counterattack = Column(Integer, comment='无视反击值')

    critical_point = Column(Integer, comment='致命点')  # 致命伤害

    damage_shield = Column(Integer, comment='免伤护盾')


# 增
def add_additional_property_record(attack_speed: int, attack: int, health: int, health_recovery: int,
                                   health_absorption: int,
                                   mana: int, mana_recovery: int, mana_absorption: int, counterattack: int,
                                   ignore_counterattack: int,
                                   critical_point: int, damage_shield: int):
    """
    新增人物、怪物常见属性记录
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
    """
    new_additional_property_record = AdditionalPropertyRecord(
        attack_speed=attack_speed, attack=attack, health=health, health_recovery=health_recovery,
        health_absorption=health_absorption,
        mana=mana, mana_recovery=mana_recovery, mana_absorption=mana_absorption, counterattack=counterattack,
        ignore_counterattack=ignore_counterattack,
        critical_point=critical_point, damage_shield=damage_shield
    )
    session.add(new_additional_property_record)
    session.commit()
    session.close()


# 删
def delete_additional_property_record(session: Session, record_id: int) -> None:
    """
    删除人物额外属性记录
    :param session: SQLAlchemy会话
    :param record_id: 记录ID
    :return: None
    """
    session.query(AdditionalPropertyRecord).filter(AdditionalPropertyRecord.id == record_id).delete()
    session.commit()


# 改

def update_additional_property_record(record_id: int, attack_speed: Optional[int] = None,
                                      attack: Optional[int] = None,
                                      health: Optional[int] = None, health_recovery: Optional[int] = None,
                                      health_absorption: Optional[int] = None,
                                      mana: Optional[int] = None, mana_recovery: Optional[int] = None,
                                      mana_absorption: Optional[int] = None,
                                      counterattack: Optional[int] = None, ignore_counterattack: Optional[int] = None,
                                      critical_point: Optional[int] = None, damage_shield: Optional[int] = None):
    """
    更新附加属性记录

    :param record_id: 记录的唯一标识
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
    :return: None
    """
    record = session.query(AdditionalPropertyRecord).get(record_id)

    if attack_speed is not None:
        record.attack_speed = attack_speed
    if attack is not None:
        record.attack = attack
    if health is not None:
        record.health = health
    if health_recovery is not None:
        record.health_recovery = health_recovery
    if health_absorption is not None:
        record.health_absorption = health_absorption
    if mana is not None:
        record.mana = mana
    if mana_recovery is not None:
        record.mana_recovery = mana_recovery
    if mana_absorption is not None:
        record.mana_absorption = mana_absorption
    if counterattack is not None:
        record.counterattack = counterattack
    if ignore_counterattack is not None:
        record.ignore_counterattack = ignore_counterattack
    if critical_point is not None:
        record.critical_point = critical_point
    if damage_shield is not None:
        record.damage_shield = damage_shield

    session.commit()


# 查
def get_additional_property_record(record_id: int) -> Optional[AdditionalPropertyRecord]:
    """
    获取人物额外属性记录
    :param record_id: 记录ID
    :return: 人物额外属性记录对象，若不存在则返回None
    """
    return session.query(AdditionalPropertyRecord).filter(AdditionalPropertyRecord.id == record_id).first()
