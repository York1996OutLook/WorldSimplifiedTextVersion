from typing import List

import datetime
import time


def get_today_timestamp(hour):
    today = datetime.datetime.now().date()
    specific_time = datetime.datetime.combine(today, datetime.time(hour))
    timestamp = int(time.mktime(specific_time.timetuple()))
    return timestamp


def find_smallest_missing(positions: List[int]):
    """
    给定一个数字数组（positions），该数组存储了一些数字，找到其中最小的不存在的数字。
    数字数组;
    例如：给定数组 [1, 2, 4, 9]，返回 3，因为 3 是不存在的最小数字。
    例如：给定数组 [1, 2, 3, 4]，返回 5，因为 5 是不存在的最小数字。
    """
    positions.sort()
    expected = 1
    for num in positions:
        if num == expected:
            expected += 1
        elif num > expected:
            return expected
    return expected


if __name__ == '__main__':
    # print(datetime.datetime.fromtimestamp(get_today_timestamp(22)).strftime('%Y-%m-%d %H:%M:%S'))

    print(find_smallest_missing([1,2,3,4,5]))