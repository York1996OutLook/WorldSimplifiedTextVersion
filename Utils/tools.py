import datetime
import time

import datetime
import time

import datetime
import time

def get_today_timestamp(hour):
    today = datetime.datetime.now().date()
    specific_time = datetime.datetime.combine(today, datetime.time(hour))
    timestamp = int(time.mktime(specific_time.timetuple()))
    return timestamp

print(datetime.datetime.fromtimestamp(get_today_timestamp(22)).strftime('%Y-%m-%d %H:%M:%S'))
