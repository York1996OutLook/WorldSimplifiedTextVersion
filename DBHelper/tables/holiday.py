from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

from Enums import CalendarType

from DBHelper.session import session

Base = declarative_base()


class Holiday(Base):
    __tablename__ = 'holiday'

    id = Column(Integer, primary_key=True)
    name = Column(String, comment="节日名字")
    month = Column(Integer, comment="月份")
    day = Column(Integer, comment="日期")

    calendar_type = Column(Integer, comment="农历还是公历，参考CalendarType")

    def __init__(self, *, name: str, month: int, day: int, calendar_type: CalendarType):
        self.name = name
        self.month = month
        self.day = day
        self.calendar_type = calendar_type


# 增
def add(*, name: str, month: int, day: int, calendar_type: CalendarType) -> Holiday:
    """
    新增一个节日
    :param name:
    :param month:
    :param day:
    :param calendar_type:
    :return:
    """
    holiday = Holiday(name=name, month=month, day=day, calendar_type=calendar_type)
    session.add(holiday)
    session.commit()
    return holiday


def add_or_update(*, name: str, month: int, day: int, calendar_type: CalendarType) -> Holiday:
    """
    根据是否存在写新增还是更新
    :param name:
    :param month:
    :param day:
    :param calendar_type:
    :return:
    """
    if is_exists_by_name(name=name):
        holiday = update_by_name(name=name, month=month, day=day, calendar_type=calendar_type)
        return holiday
    holiday = add(name=name, month=month, day=day, calendar_type=calendar_type)
    return holiday


# 删

# 改
def update_by_name(*, name: str, month: int, day: int, calendar_type: CalendarType) -> Holiday:
    """
    根据name进行更新。后期可能会增加
    :param name:
    :param month:
    :param day:
    :param calendar_type:
    :return:
    """
    holiday = session.query(Holiday).filter(Holiday.name == name).first()
    holiday.month = month
    holiday.day = day
    holiday.calendar_type = calendar_type
    session.commit()
    return holiday


# 查
def is_exists_by_name(*, name: str):
    """
    判断是否存在
    :param name:
    :return:
    """
    holiday = session.query(Holiday).filter(Holiday.name == name).first()
    return holiday is not None


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
