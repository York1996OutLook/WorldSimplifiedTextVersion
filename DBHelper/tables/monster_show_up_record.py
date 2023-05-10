import datetime
from typing import List, Set

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Float, Boolean

from DBHelper.session import session
from DBHelper.tables.base_table import Basic,Base
from DBHelper.tables.base_table import CustomColumn

from Enums import DateType



class MonsterShowUpRecord(Basic,Base):
    """
    怪物出现的日期,会将所有结果进行合并,然后出现;
    """
    __cn__ = "怪物出现记录"

    __tablename__ = 'monster_show_up_record'

    monster_id = CustomColumn(Integer,cn="怪物ID", comment='怪物id')

    date_type = CustomColumn(Integer,cn="日期类型", comment="出现的日期类型,DateType")
    date_value = CustomColumn(Integer,cn='日期', comment="确定date_type后,再确定具体的时间")

    @classmethod
    def add_or_update_by_id(cls, *,
                       monster_id: int=None,
                       date_type: int=None,
                       date_value: int=None
                       ):

        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
        return record


# 删
def del_all_by_monster_id(*,
                          monster_id: int):
    """
    删除某个monster的所有出现日期记录。方便后续新增记录。
    :param monster_id:
    :return:
    """
    session.query(MonsterShowUpRecord).filter(MonsterShowUpRecord.monster_id == monster_id).delete()
    session.commit()


# 改

# 查

def get_all_by_week_day(*,
                        week_day: int
                        ) -> List[MonsterShowUpRecord]:
    records = session.query(MonsterShowUpRecord).filter(MonsterShowUpRecord.date_type == DateType.DAY_OF_WEEK,
                                                        MonsterShowUpRecord.date_value == week_day).all()
    return records


def get_all_by_month_day(*,
                         month_day: int
                         ) -> List[MonsterShowUpRecord]:
    records = session.query(MonsterShowUpRecord).filter(MonsterShowUpRecord.date_type == DateType.DAY_OF_MONTH,
                                                        MonsterShowUpRecord.date_value == month_day).all()
    return records


def get_all_by_holiday(*,
                       holiday: int
                       ) -> List[MonsterShowUpRecord]:
    records = session.query(MonsterShowUpRecord).filter(MonsterShowUpRecord.date_type == DateType.HOLIDAY,
                                                        MonsterShowUpRecord.date_value == holiday).all()
    return records


def get_all_by_today() -> List[MonsterShowUpRecord]:
    records = []
    records.extend(get_all_by_week_day(week_day=(datetime.datetime.now().weekday()+1)%7))
    records.extend(get_all_by_month_day(month_day=datetime.datetime.now().day))
    # todo: 添加对节日得支持
    # records.extend(get_all_by_holiday(holiday=datetime.datetime.now().day))
    return records


# other
def get_all_monster_id_by_today() -> Set[int]:
    records = get_all_by_today()
    shows_up_monster_ids = {record.monster_id for record in records}
    return shows_up_monster_ids
