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

    def __init__(self, *, monster_id: int, date_type: int, date_value: int):
        self.monster_id = monster_id
        self.date_type = date_type
        self.date_value = date_value


# 增
def add(*, monster_id: int, date_type: int, date_value: int):
    """

    :param monster_id:
    :param date_type:
    :param date_value:
    :return:
    """
    shows_up_record = MonsterShowUpRecord(monster_id=monster_id,
                                          date_type=date_type,
                                          date_value=date_value
                                          )
    session.add(shows_up_record)
    session.commit()


# 删
def del_all_by_monster_id(*, monster_id: int):
    """
    删除某个monster的所有出现日期记录。方便后续新增记录。
    :param monster_id:
    :return:
    """
    session.query(MonsterShowUpRecord).filter(MonsterShowUpRecord.monster_id == monster_id).delete()
    session.commit()
# 改

# 查
