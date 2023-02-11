from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from typing import List

Base = declarative_base()

from DBHelper.session import session


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

def get_success_prob_by_star_count(star_count: str) -> str:
    """
    根据升星数量查询成功概率

    :param star_count: 升星数量
    :return: 成功概率
    """

    prob = session.query(RaiseStarProb).filter_by(star_count=star_count).first()
    return prob.success_prob