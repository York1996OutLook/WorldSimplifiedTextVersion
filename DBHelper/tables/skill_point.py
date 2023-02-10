from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Optional

Base = declarative_base()

from ..session import session


class SkillPoint(Base):
    """
    升级技能需要的技能点
    """
    __tablename__ = 'skill_point'
    id = Column(Integer, primary_key=True)
    level = Column(Integer, comment="等级")
    need_point = Column(Integer, comment="所需技能点")


# 增

# 删

# 改

# 查

def get_kill_point_by_level(level: int, ):
    """
    获取某个等级需要的技能点
    """
    skill_point = session.query(SkillPoint).filter(SkillPoint.level == level)
    return skill_point
