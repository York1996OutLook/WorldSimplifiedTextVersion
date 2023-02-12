from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Optional
from DBHelper.session import session

Base = declarative_base()


class PositiveSkillCostMana(Base):
    """
    使用技能所需要的蓝量
    """
    __tablename__ = 'positive_skill_cost_mana'
    id = Column(Integer, primary_key=True)

    skill_id = Column(Integer, comment="技能ID")
    level = Column(Integer, comment="等级")
    need_point = Column(Integer, comment="所需技能点")


# 增

# 删

# 改

# 查

def get_kill_cost_mana_by_level(*,
                                skill_id: int,
                                level: int, ):
    """
    获取某个技能等级需要的法力值记录
    """
    skill_cost_mana = session.query(PositiveSkillCostMana).filter(
        PositiveSkillCostMana.skill_id == skill_id,
        PositiveSkillCostMana.level == level
    )
    return skill_cost_mana
