from typing import List

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session

Base = declarative_base()


class OpenDecomposeOrDropStuffsRecord(Base):
    """
    打开 分解 掉落的物品记录
    """
    __tablename__ = 'stuff_record'
    id = Column(Integer, primary_key=True)

    get_stuff_type = Column(Integer, comment="物品的类型，参考枚举类型StuffType。查询的时候，现根")  # 参考枚举类型
    get_stuff_id = Column(Integer, comment="物品的ID")  # 参考物品id
    get_stuff_prob = Column(Integer, comment="出现的概率，独立计算概率。比如50%A物品，50%B物品，最后的结果可能是空，A，B,A+B四种情况！")

