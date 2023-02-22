from typing import List, Optional

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

from DBHelper.session import session

Base = declarative_base()


class MonsterSkillRecord(Base):
    """
    已学习技能表。只存储最大等级。可能会被更新；
    """
    __tablename__ = 'monster_skill_record'

    id = Column(Integer, primary_key=True)

    monster_id = Column(Integer, comment="monster_id")  # 参考人物表

    skill_id = Column(Integer, comment="技能ID")  # ForeignKey(Skill.id)
    skill_level = Column(Integer, comment="已经学习的技能等级")

# 增

# 删

# 改

# 查