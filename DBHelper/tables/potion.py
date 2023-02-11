from typing import List

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session

Base = declarative_base()


# 成就系统
class Potion(Base):
    """
    药剂
    """
    __tablename__ = "potion"

    id = Column(Integer, primary_key=True, comment="药剂ID")
    name = Column(String, comment="药剂名称")

    duration_by_min = Column(Integer, comment="有效期，以分钟为单位")
    introduce = Column(String, comment="药剂的介绍")


# 增

# 删

# 改

# 查
def get_potion_by_potion_id(*,potion_id: int) -> Potion:
    """
    根据potion的id查询你potion
    """
    potion = session.query(Potion).filter(Potion.id == potion_id)
    return potion
