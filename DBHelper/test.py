import dateutil
from dateutil import easter
from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
import dateutil.relativedelta as relativedelta
from datetime import date, timedelta
import datetime
from dateutil.rrule import rrule, MONTHLY


def get_thanksgiving_day(year):
    # 计算每年感恩节的日期
    target_thanksgiving_day = datetime.date(year, 11, 1)
    days_to_add = (3 - target_thanksgiving_day.weekday()) % 7
    target_thanksgiving_day += datetime.timedelta(days=days_to_add)
    return thanksgiving_day


year = 2023

valentine_day = date(year, 2, 14)
arbor_day = date(year, 3, 12)
april_fool_day = date(year, 4, 1)
easter_day = easter.easter(year)
halloween_day = date(year, 10, 31)
thanksgiving_day = get_thanksgiving_day(year)
