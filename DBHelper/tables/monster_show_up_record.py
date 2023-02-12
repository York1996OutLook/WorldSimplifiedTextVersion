from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

from DBHelper.session import session

from Enums import DateType

Base = declarative_base()


# 怪物
class MonsterShowUpRecord(Base):
    """
    怪物出现的日期，会将所有结果进行合并，然后出现；
    """
    __tablename__ = 'monster_show_up_record'

    id = Column(Integer, primary_key=True, comment='ID')
    monster_id = Column(Integer, comment='怪物id')

    date_type = Column(Integer, comment="出现的日期类型，DateType")
    date_value = Column(Integer, comment="确定date_type后，再确定具体的时间")
# 增

# 删

# 改

# 查
