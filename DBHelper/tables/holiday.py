from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Float, Boolean,Text

from Enums import CalendarType

from DBHelper.session import session
from DBHelper.tables.base_table import Entity
from DBHelper.tables.base_table import CustomColumn

Base = declarative_base()


class Holiday(Entity,Base):
    __cn__ = "节日"
    __tablename__ = 'holiday'
    name = CustomColumn(String, cn='名称')  # 显式复制并设置 cn 属性

    month = CustomColumn(Integer,cn="月份", comment="月份")
    day = CustomColumn(Integer,cn="日期", comment="日期")

    calendar_type = CustomColumn(Integer,cn="历法", comment="农历还是公历,参考CalendarType")
    introduce = CustomColumn(Text, cn="介绍")

    @classmethod
    def add_or_update_by_name(cls,
                              *,
                              name: str,
                              month: int = None,
                              day: int = None,
                              calendar_type: int = None,
                              ) -> "Holiday":
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_name)
        record = cls._add_or_update_by_name(**fields)
        return record

    @classmethod
    def add_or_update_by_id(
            cls,
            *,
            _id: int,

            name: str = None,
            month: int = None,
            day: int = None,
            calendar_type: int = None,
    ) -> "Holiday":
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
        return record


if __name__ == '__main__':
    lunar_holidays_list = [
        {
            'name': '春节',
            'month': 1,
            'day': 1,
        },
        {
            'name': '元宵节',
            'month': 1,
            'day': 15,
        },
        {
            'name': '龙抬头',
            'month': 2,
            'day': 2,
        },
        {
            'name': '端午节',
            'month': 5,
            'day': 5,
        },
        {
            'name': '七夕节',
            'month': 7,
            'day': 7,
        },
        {
            'name': '中元节',
            'month': 7,
            'day': 15,
        },
        {
            'name': '中秋节',
            'month': 8,
            'day': 15,
        },
        {
            'name': '重阳节',
            'month': 9,
            'day': 9,
        },
        {
            'name': '腊八节',
            'month': 12,
            'day': 8,
        },
    ]

    gregorian_holidays_list = [
        {
            "name": "元旦",
            "month": 1,
            "day": 1,
        },
        {
            "name": "情人节",
            "month": 2,
            "day": 14,
        },
        {
            "name": "植树节",
            "month": 3,
            "day": 12,
        },
        {
            "name": "愚人节",
            "month": 4,
            "day": 1,
        },
        {
            "name": "清明节",
            "month": 4,
            "day": 5,
        },
        {
            "name": "国庆节",
            "month": 10,
            "day": 1,
        },
        {
            "name": "万圣节",
            "month": 10,
            "day": 31,
        },
        {
            "name": "光棍节",
            "month": 11,
            "day": 11,
        },
        {
            "name": "圣诞节",
            "month": 12,
            "day": 25,
        },
    ]

    for lunar_holiday in lunar_holidays_list:
        add_or_update(name=lunar_holiday['name'],
                      month=lunar_holiday['month'],
                      day=lunar_holiday['day'],
                      calendar_type=CalendarType.LUNAR, )
    for lunar_holiday in lunar_holidays_list:
        add_or_update(name=lunar_holiday['name'],
                      month=lunar_holiday['month'],
                      day=lunar_holiday['day'],
                      calendar_type=CalendarType.GREGORIAN, )
