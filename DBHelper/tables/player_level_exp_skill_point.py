from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Float, Boolean, func, desc

from typing import Optional, List

from DBHelper.session import session
from DBHelper.tables.base_table import Basic,Base
from DBHelper.tables.base_table import CustomColumn



class PlayerLevelExpSkillPoint(Basic,Base):
    """
    升级所需经验
    """
    __cn__ = "升级经验、技能点"
    __tablename__ = "player_level_exp_skill_point"
    id = CustomColumn(Integer, cn="ID", primary_key=True, editable=False,autoincrement=True)

    level = CustomColumn(Integer, cn="等级",comment="等级")
    required_exp = CustomColumn(Integer, cn="所需经验",comment="所需经验。非叠加;")
    skill_point = CustomColumn(Integer, cn="技能点",comment="升到该等级能够获得的技能点数量")

    @classmethod
    def add_or_update_by_id(cls, *,
                       _id: int,
                       level: int = None,
                       required_exp: int = None,
                       skill_point: int = None
                       ):
        """
        更新或创建等级及对应经验技能点记录
        :param _id: 记录ID
        :param level: 等级
        :param required_exp: 所需经验
        :param skill_point: 能够获得的技能点数量
        :return:
        """
        record = cls._add_or_update_by_id(kwargs=locals())
        return record

    @classmethod
    def get_by_level(cls, level: int) -> "PlayerLevelExpSkillPoint":
        """
        通过等级获取对应记录
        :param level: 等级
        :return: PlayerLevelExpSkillPoint
        """
        record=cls.get_by_id()
        record = session.query(cls).filter(cls.level == level).first()
        return record



# 删
def delete(level_id: int) -> None:
    """
    删除某个等级的经验需求

    :param level_id: 要删除的等级的ID
    :return: None
    """
    record = session.query(PlayerLevelExpSkillPoint).filter(PlayerLevelExpSkillPoint.id == level_id)
    session.commit()
    return record


# 查
def get_by_level(level: int) -> PlayerLevelExpSkillPoint:
    """
    :param level: 等级
    :return:
    """
    return session.query(PlayerLevelExpSkillPoint).filter(PlayerLevelExpSkillPoint.level == level).first()


def get_max_level() -> int:
    """
    获取总经验值
    """
    max_level = session.query(PlayerLevelExpSkillPoint.level).order_by(desc(PlayerLevelExpSkillPoint.level)).first()
    return max_level


def get_total_exp():
    """
    获取总经验值
    """
    total_exp = session.query(func.sum(PlayerLevelExpSkillPoint.required_exp)).scalar()
    return total_exp


if __name__ == '__main__':
    exps = [
        PlayerLevelExpSkillPoint(level=2, required_exp=10, skill_point=50),
        PlayerLevelExpSkillPoint(level=3, required_exp=45, skill_point=50),
        PlayerLevelExpSkillPoint(level=4, required_exp=140, skill_point=50),
        PlayerLevelExpSkillPoint(level=5, required_exp=325, skill_point=50),
        PlayerLevelExpSkillPoint(level=6, required_exp=630, skill_point=50),
        PlayerLevelExpSkillPoint(level=7, required_exp=1100, skill_point=50),
        PlayerLevelExpSkillPoint(level=8, required_exp=1700, skill_point=50),
        PlayerLevelExpSkillPoint(level=9, required_exp=2500, skill_point=50),
        PlayerLevelExpSkillPoint(level=10, required_exp=3600, skill_point=50),
        PlayerLevelExpSkillPoint(level=11, required_exp=5000, skill_point=50),
        PlayerLevelExpSkillPoint(level=12, required_exp=6600, skill_point=50),
        PlayerLevelExpSkillPoint(level=13, required_exp=8600, skill_point=50),
        PlayerLevelExpSkillPoint(level=14, required_exp=11000, skill_point=50),
        PlayerLevelExpSkillPoint(level=15, required_exp=13000, skill_point=50),
        PlayerLevelExpSkillPoint(level=16, required_exp=16000, skill_point=50),
        PlayerLevelExpSkillPoint(level=17, required_exp=20000, skill_point=50),
        PlayerLevelExpSkillPoint(level=18, required_exp=24000, skill_point=50),
        PlayerLevelExpSkillPoint(level=19, required_exp=29000, skill_point=50),
        PlayerLevelExpSkillPoint(level=20, required_exp=34000, skill_point=50),
        PlayerLevelExpSkillPoint(level=21, required_exp=50000, skill_point=50),
        PlayerLevelExpSkillPoint(level=22, required_exp=95000, skill_point=50),
        PlayerLevelExpSkillPoint(level=23, required_exp=120000, skill_point=50),
        PlayerLevelExpSkillPoint(level=24, required_exp=150000, skill_point=50),
        PlayerLevelExpSkillPoint(level=25, required_exp=187000, skill_point=50),
        PlayerLevelExpSkillPoint(level=26, required_exp=201000, skill_point=50),
        PlayerLevelExpSkillPoint(level=27, required_exp=222000, skill_point=50),
        PlayerLevelExpSkillPoint(level=28, required_exp=259000, skill_point=50),
        PlayerLevelExpSkillPoint(level=29, required_exp=300000, skill_point=50),
        PlayerLevelExpSkillPoint(level=30, required_exp=360000, skill_point=50),
        PlayerLevelExpSkillPoint(level=31, required_exp=430000, skill_point=50),
        PlayerLevelExpSkillPoint(level=32, required_exp=510000, skill_point=50),
        PlayerLevelExpSkillPoint(level=33, required_exp=600000, skill_point=50),
        PlayerLevelExpSkillPoint(level=34, required_exp=700000, skill_point=50),
        PlayerLevelExpSkillPoint(level=35, required_exp=810000, skill_point=50),
        PlayerLevelExpSkillPoint(level=36, required_exp=920000, skill_point=50),
        PlayerLevelExpSkillPoint(level=37, required_exp=1030000, skill_point=50),
        PlayerLevelExpSkillPoint(level=38, required_exp=1150000, skill_point=50),
        PlayerLevelExpSkillPoint(level=39, required_exp=1280000, skill_point=50),
        PlayerLevelExpSkillPoint(level=40, required_exp=1420000, skill_point=50),
        PlayerLevelExpSkillPoint(level=41, required_exp=1570000, skill_point=50),
        PlayerLevelExpSkillPoint(level=42, required_exp=1730000, skill_point=50),
        PlayerLevelExpSkillPoint(level=43, required_exp=1800000, skill_point=50),
        PlayerLevelExpSkillPoint(level=44, required_exp=1980000, skill_point=50),
        PlayerLevelExpSkillPoint(level=45, required_exp=2070000, skill_point=50),
        PlayerLevelExpSkillPoint(level=46, required_exp=2270000, skill_point=50),
        PlayerLevelExpSkillPoint(level=47, required_exp=2480000, skill_point=50),
        PlayerLevelExpSkillPoint(level=48, required_exp=2600000, skill_point=50),
        PlayerLevelExpSkillPoint(level=49, required_exp=2930000, skill_point=50),
        PlayerLevelExpSkillPoint(level=50, required_exp=3170000, skill_point=50),
        PlayerLevelExpSkillPoint(level=51, required_exp=3420000, skill_point=50),
        PlayerLevelExpSkillPoint(level=52, required_exp=3680000, skill_point=50),
        PlayerLevelExpSkillPoint(level=53, required_exp=3950000, skill_point=50),
        PlayerLevelExpSkillPoint(level=54, required_exp=4220000, skill_point=50),
        PlayerLevelExpSkillPoint(level=55, required_exp=4350000, skill_point=50),
        PlayerLevelExpSkillPoint(level=56, required_exp=4500000, skill_point=50),
        PlayerLevelExpSkillPoint(level=57, required_exp=4670000, skill_point=50),
        PlayerLevelExpSkillPoint(level=58, required_exp=4850000, skill_point=50),
        PlayerLevelExpSkillPoint(level=59, required_exp=5050000, skill_point=50),
        PlayerLevelExpSkillPoint(level=60, required_exp=5270000, skill_point=50),
        PlayerLevelExpSkillPoint(level=61, required_exp=5510000, skill_point=50),
        PlayerLevelExpSkillPoint(level=62, required_exp=5780000, skill_point=50),
        PlayerLevelExpSkillPoint(level=63, required_exp=6080000, skill_point=50),
        PlayerLevelExpSkillPoint(level=64, required_exp=6400000, skill_point=50),
        PlayerLevelExpSkillPoint(level=65, required_exp=6750000, skill_point=50),
        PlayerLevelExpSkillPoint(level=66, required_exp=7140000, skill_point=50),
        PlayerLevelExpSkillPoint(level=67, required_exp=7570000, skill_point=50),
        PlayerLevelExpSkillPoint(level=68, required_exp=8050000, skill_point=50),
        PlayerLevelExpSkillPoint(level=69, required_exp=8570000, skill_point=50),
        PlayerLevelExpSkillPoint(level=70, required_exp=9140000, skill_point=50),
        PlayerLevelExpSkillPoint(level=71, required_exp=9770000, skill_point=50),
        PlayerLevelExpSkillPoint(level=72, required_exp=10460000, skill_point=50),
        PlayerLevelExpSkillPoint(level=73, required_exp=11220000, skill_point=50),
        PlayerLevelExpSkillPoint(level=74, required_exp=12060000, skill_point=50),
        PlayerLevelExpSkillPoint(level=75, required_exp=12980000, skill_point=50),
        PlayerLevelExpSkillPoint(level=76, required_exp=14000000, skill_point=50),
        PlayerLevelExpSkillPoint(level=77, required_exp=15110000, skill_point=50),
        PlayerLevelExpSkillPoint(level=78, required_exp=16340000, skill_point=50),
        PlayerLevelExpSkillPoint(level=79, required_exp=17690000, skill_point=50),
        PlayerLevelExpSkillPoint(level=80, required_exp=19170000, skill_point=50),
        PlayerLevelExpSkillPoint(level=81, required_exp=20810000, skill_point=50),
        PlayerLevelExpSkillPoint(level=82, required_exp=22600000, skill_point=50),
        PlayerLevelExpSkillPoint(level=83, required_exp=24580000, skill_point=50),
        PlayerLevelExpSkillPoint(level=84, required_exp=26750000, skill_point=50),
        PlayerLevelExpSkillPoint(level=85, required_exp=29140000, skill_point=50),
        PlayerLevelExpSkillPoint(level=86, required_exp=31770000, skill_point=50),
        PlayerLevelExpSkillPoint(level=87, required_exp=34660000, skill_point=50),
        PlayerLevelExpSkillPoint(level=88, required_exp=37850000, skill_point=50),
        PlayerLevelExpSkillPoint(level=89, required_exp=41350000, skill_point=50),
        PlayerLevelExpSkillPoint(level=90, required_exp=45200000, skill_point=50),
        PlayerLevelExpSkillPoint(level=91, required_exp=49430000, skill_point=50),
        PlayerLevelExpSkillPoint(level=92, required_exp=54090000, skill_point=50),
        PlayerLevelExpSkillPoint(level=93, required_exp=59210000, skill_point=50),
        PlayerLevelExpSkillPoint(level=94, required_exp=64850000, skill_point=50),
        PlayerLevelExpSkillPoint(level=95, required_exp=71050000, skill_point=50),
        PlayerLevelExpSkillPoint(level=96, required_exp=77870000, skill_point=50),
        PlayerLevelExpSkillPoint(level=97, required_exp=85370000, skill_point=50),
        PlayerLevelExpSkillPoint(level=98, required_exp=93630000, skill_point=50),
        PlayerLevelExpSkillPoint(level=99, required_exp=102700000, skill_point=50),
        PlayerLevelExpSkillPoint(level=100, required_exp=112690000, skill_point=50),
        PlayerLevelExpSkillPoint(level=101, required_exp=123680000, skill_point=50),
        PlayerLevelExpSkillPoint(level=102, required_exp=135760000, skill_point=50),
        PlayerLevelExpSkillPoint(level=103, required_exp=149050000, skill_point=50),
        PlayerLevelExpSkillPoint(level=104, required_exp=163670000, skill_point=50),
        PlayerLevelExpSkillPoint(level=105, required_exp=179750000, skill_point=50),
        PlayerLevelExpSkillPoint(level=106, required_exp=197440000, skill_point=50),
        PlayerLevelExpSkillPoint(level=107, required_exp=216900000, skill_point=50),
        PlayerLevelExpSkillPoint(level=108, required_exp=238310000, skill_point=50),
        PlayerLevelExpSkillPoint(level=109, required_exp=261860000, skill_point=50),
        PlayerLevelExpSkillPoint(level=110, required_exp=287760000, skill_point=50),
    ]
    session.add_all(exps)
    session.commit()
