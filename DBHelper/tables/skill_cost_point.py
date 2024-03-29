from sqlalchemy import Integer, String
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Optional

from DBHelper.session import session
from DBHelper.tables.base_table import Basic,Base
from DBHelper.tables.base_table import CustomColumn


class SkillCostPoint(Basic,Base):
    """
    升级技能需要的技能点；
    10个技能全部学满，10*450=4500技能点；
    每升一级给50个技能点，90级的时候，能够学完所有技能；
    """
    __cn__ = "技能消耗技能点"
    __tablename__ = 'skill_cost_point'
    id = CustomColumn(Integer, cn="ID", primary_key=True, editable=False,autoincrement=True)

    level = CustomColumn(Integer, cn="等级",comment="等级")
    need_point = CustomColumn(Integer, cn="技能点",comment="所需技能点")

    @classmethod
    def add_or_update_by_id(
            cls,
            *,
            _id: int,

            level: int = None,
            need_point: int = None,
    ):
        record = cls._add_or_update_by_id(kwargs=locals())
        return record
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
