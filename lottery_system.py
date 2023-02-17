from collections import defaultdict
from typing import List

from DBHelper.db import *

from Enums import AdditionSourceType, AdditionalPropertyType, BasePropertyType
from Utils import tools


def get_today_lottery_winners():
    """
    获取
    """
    # 获取今天可以抽奖时间段内的最大号码
    start_hour, end_hour =setting.get_lottery_start_hour(), setting.get_lottery_end_hour()

    today_start_timestamp = tools.get_today_timestamp(hour=start_hour)
    today_end_timestamp = tools.get_today_timestamp(hour=end_hour)

    # 获取当日最大号码的记录
    all_max_num_player_lottery_records = player_lottery_record.get_all_records_with_max_num_by_timestamp_range(
        start_timestamp=today_start_timestamp,
        end_timestamp=today_end_timestamp
    )

    # 获取当日抽的幸运数字的记录
    all_is_lucky_num_player_lottery_records = player_lottery_record.get_all_is_lucky_num_records_by_timestamp_range(
        start_timestamp=today_start_timestamp,
        end_timestamp=today_end_timestamp
    )

    character_ids = set()
    for record in [*all_max_num_player_lottery_records, *all_is_lucky_num_player_lottery_records]:
        character_ids.add(record.character_id)

    return character_ids
