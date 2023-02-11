

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

Base = declarative_base()

from DBHelper.session import session



# 怪物
class MonsterShowUpRecord(Base):
    """
    怪物出现的日期，会将所有结果进行合并，然后出现；
    """
    __tablename__ = 'monster_show_up_record'

    id = Column(Integer, primary_key=True, comment='ID')
    monster_id = Column(Integer, comment='怪物id')

    weekday = Column(String, comment="周几会出现")
    monthday = Column(String, comment="每个月几号会出现")
    special_day = Column(String,comment="特殊日期会出现")


# 增

# 删

# 改

# 查