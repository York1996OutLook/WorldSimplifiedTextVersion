from collections import defaultdict
import time
from typing import List

from Enums import AdditionSourceType, AdditionalPropertyType, BeingType
from DBHelper.db import *
from DBHelper.session import session
from Utils import tools


def get_player_unexpired_potion_record_by_character_id(*,
                                                    character_id: int
                                                    )->player_potion_record.PlayerPotionRecord:
    """
    Retrieve information about a specific potion record

    :param character_id: ID of the potion record
    :return: Dictionary with information about the potion record, None if no record found
    """
    current_timestamp = int(time.time())
    potion_record = player_potion_record.get_player_potion_record_by_character_id(character_id=character_id)

    # 如果没有对应的记录，返回None
    if potion_record is None:
        return None
    one_potion = potion.get_potion_by_potion_id(potion_id=potion_record.potion_id)
    duration_by_timestamp = tools.convert_to_milliseconds(minutes=one_potion.duration_by_min)

    # 使用时间+药效持续时间<当前时间 视为有效；
    record = player_potion_record.PlayerPotionRecord.query.filter(
        potion_record.take_timestamp + duration_by_timestamp <= current_timestamp).first()
    return record
