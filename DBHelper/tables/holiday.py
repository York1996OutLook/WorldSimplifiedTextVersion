

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

from Enums import CalendarType

Base = declarative_base()

from DBHelper.session import session


class Holiday(Base):
    __tablename__ = 'holiday'

    id = Column(Integer, primary_key=True)
    name = Column(String, comment="节日名字")
    month = Column(Integer, comment="月份")
    day = Column(Integer, comment="日期")

    calendar_type = Column(Integer, comment="农历还是公历，参考CalendarType")


# 增

# 删

# 改

# 查


if __name__ == '__main__':
    session.add(Holiday(name="春节", month=1, day=1, calendar_type=0))
    session.add(Holiday(name="元宵节", month=1, day=15, calendar_type=0))
    session.add(Holiday(name="龙抬头", month=2, day=2, calendar_type=0))
    session.add(Holiday(name="端午节", month=5, day=5, calendar_type=0))
    session.add(Holiday(name="七夕节", month=7, day=7, calendar_type=0))
    session.add(Holiday(name="中元节", month=7, day=15, calendar_type=0))
    session.add(Holiday(name="中秋节", month=8, day=15, calendar_type=0))
    session.add(Holiday(name="重阳节", month=9, day=9, calendar_type=0))
    session.add(Holiday(name="腊八节", month=12, day=8, calendar_type=0))
    session.add(Holiday(name="除夕", month=12, day=29, calendar_type=0))

    session.add(Holiday(name="元旦", month=1, day=1, calendar_type=1))
    session.add(Holiday(name="情人节", month=2, day=14, calendar_type=1))
    session.add(Holiday(name="愚人节", month=4, day=1, calendar_type=1))
    session.add(Holiday(name="清明节", month=4, day=5, calendar_type=1))
    session.add(Holiday(name="国庆节", month=10, day=1, calendar_type=1))
    session.add(Holiday(name="万圣节", month=10, day=31, calendar_type=1))
    session.add(Holiday(name="光棍节", month=11, day=11, calendar_type=1))
    session.add(Holiday(name="圣诞节", month=12, day=25, calendar_type=1))
    session.commit()
