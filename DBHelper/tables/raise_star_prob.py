from typing import List

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session

Base = declarative_base()


class RaiseStarProb(Base):
    """
    升星概率表

    """
    __tablename__ = 'raise_star_prob'

    id = Column(Integer, primary_key=True)
    star_count = Column(String, comment="当前升星数量")
    success_prob = Column(String, comment="从上一星星数量升级到当前数量的星星成功的概率，100为决定成功，0是无法成功")


# 增

# 删

# 改

# 查

def get_success_prob_by_star_count(*,
                                   star_count: str) -> str:
    """
    根据升星数量查询成功概率

    :param star_count: 升星数量
    :return: 成功概率
    """

    prob = session.query(RaiseStarProb).filter_by(star_count=star_count).first()
    return prob.success_prob


if __name__ == '__main__':
    probs = [
        RaiseStarProb(star_count=1, success_prob=100),
        RaiseStarProb(star_count=2, success_prob=100),
        RaiseStarProb(star_count=3, success_prob=100),
        RaiseStarProb(star_count=4, success_prob=100),
        RaiseStarProb(star_count=5, success_prob=100),
        RaiseStarProb(star_count=6, success_prob=97),
        RaiseStarProb(star_count=7, success_prob=94),
        RaiseStarProb(star_count=8, success_prob=91),
        RaiseStarProb(star_count=9, success_prob=88),
        RaiseStarProb(star_count=10, success_prob=85),
        RaiseStarProb(star_count=11, success_prob=82),
        RaiseStarProb(star_count=12, success_prob=79),
        RaiseStarProb(star_count=13, success_prob=76),
        RaiseStarProb(star_count=14, success_prob=73),
        RaiseStarProb(star_count=15, success_prob=70),
        RaiseStarProb(star_count=16, success_prob=67),
        RaiseStarProb(star_count=17, success_prob=64),
        RaiseStarProb(star_count=18, success_prob=61),
        RaiseStarProb(star_count=19, success_prob=58),
        RaiseStarProb(star_count=20, success_prob=55),
        RaiseStarProb(star_count=21, success_prob=52),
        RaiseStarProb(star_count=22, success_prob=49),
        RaiseStarProb(star_count=23, success_prob=46),
        RaiseStarProb(star_count=24, success_prob=43),
        RaiseStarProb(star_count=25, success_prob=40),
        RaiseStarProb(star_count=26, success_prob=37),
        RaiseStarProb(star_count=27, success_prob=34),
        RaiseStarProb(star_count=28, success_prob=31),
        RaiseStarProb(star_count=29, success_prob=28),
        RaiseStarProb(star_count=30, success_prob=25),
        RaiseStarProb(star_count=31, success_prob=22),
        RaiseStarProb(star_count=32, success_prob=19),
        RaiseStarProb(star_count=33, success_prob=16),
        RaiseStarProb(star_count=34, success_prob=13),
        RaiseStarProb(star_count=35, success_prob=10),
        RaiseStarProb(star_count=36, success_prob=7),
        RaiseStarProb(star_count=37, success_prob=4),
        RaiseStarProb(star_count=38, success_prob=1),
        RaiseStarProb(star_count=39, success_prob=1),
        RaiseStarProb(star_count=40, success_prob=1),
        RaiseStarProb(star_count=41, success_prob=1),
        RaiseStarProb(star_count=42, success_prob=1),
        RaiseStarProb(star_count=43, success_prob=1),
        RaiseStarProb(star_count=44, success_prob=1),
        RaiseStarProb(star_count=45, success_prob=1),
        RaiseStarProb(star_count=46, success_prob=1),
        RaiseStarProb(star_count=47, success_prob=1),
        RaiseStarProb(star_count=48, success_prob=1),
        RaiseStarProb(star_count=49, success_prob=1),
        RaiseStarProb(star_count=50, success_prob=1),
        RaiseStarProb(star_count=51, success_prob=0),
    ]

    session.add_all(probs)
    session.commit()
