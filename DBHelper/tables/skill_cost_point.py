from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Optional

from DBHelper.session import session

Base = declarative_base()


class SkillCostPoint(Base):
    """
    升级技能需要的技能点；
    10个技能全部学满，10*450=4500技能点；
    每升一级给50个技能点，90级的时候，能够学完所有技能；
    """
    __tablename__ = 'skill_point'
    id = Column(Integer, primary_key=True)
    level = Column(Integer, comment="等级")
    need_point = Column(Integer, comment="所需技能点")


# 增

# 删

# 改

# 查

def get_kill_point_by_level(*,
                            level: int, ):
    """
    获取某个等级需要的技能点
    """
    skill_point = session.query(SkillCostPoint).filter(SkillCostPoint.level == level)
    return skill_point


if __name__ == '__main__':
    skill_cost_points = [
        SkillCostPoint(level=1, required_exp=10, need_point=5),
        SkillCostPoint(level=2, required_exp=10, need_point=15),
        SkillCostPoint(level=3, required_exp=45, need_point=25),
        SkillCostPoint(level=4, required_exp=140, need_point=30),
        SkillCostPoint(level=5, required_exp=325, need_point=35),
        SkillCostPoint(level=6, required_exp=630, need_point=40),
        SkillCostPoint(level=7, required_exp=1100, need_point=45),
        SkillCostPoint(level=8, required_exp=1700, need_point=50),
        SkillCostPoint(level=9, required_exp=2500, need_point=55),
    ]
    session.add_all(skill_cost_points)
    session.commit()
