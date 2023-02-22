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

    def __init__(self, *, monster_id: int, skill_id: int, skill_level: int):
        self.monster_id = monster_id
        self.skill_id = skill_id
        self.skill_level = skill_level


# 增
def add(*, monster_id: int, skill_id: int, skill_level: int) -> MonsterSkillRecord:
    record = MonsterSkillRecord(monster_id=monster_id, skill_id=skill_id, skill_level=skill_level)
    session.add(record)
    session.refresh(record)
    return record


# 删
def del_monster_skill(*, monster_id: int):
    session.query(MonsterSkillRecord).filter(MonsterSkillRecord.monster_id == monster_id).delete()
    return True


# 改
def update(*, monster_id: int, skill_id: int, skill_level: int) -> MonsterSkillRecord:
    record = session.query(MonsterSkillRecord).filter(MonsterSkillRecord.monster_id == monster_id).first()
    record.skill_id = skill_id
    record.skill_level = skill_level
    return record

# 查
