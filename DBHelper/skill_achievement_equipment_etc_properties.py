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


class SkillAchievementEquipmentEtcProperties(Base):
    """技能、装备、成就等常见的所有属性表，后期可能会更新"""
    __tablename__ = 'skill_achievement_equipment_etc_properties'

    id = Column(Integer, primary_key=True)

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