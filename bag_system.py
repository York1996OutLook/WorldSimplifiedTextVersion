from collections import defaultdict, OrderedDict
import time
from typing import List

from sqlalchemy import Boolean
from DBHelper.db import *

from Enums import AdditionSourceType, AdditionalPropertyType, BasePropertyType, MailType
from Utils import tools

from DBHelper.session import session


def player_sort_bag(*,character_id: int):
    """
    对玩家的背包进行排序，重新安排背包中物品的位置；
    :param character_id:
    :return:
    """
    bag_stuffs = player_stuff_record.get_all_in_bag_stuffs_by_character_id(character_id=character_id)

    # order by stuff.type stuff.name
    bag_stuffs_list = []
    for bag_stuff in bag_stuffs:
        stuff = player_stuff_record.get_by_record_id(record_id=bag_stuff.id)
        bag_stuffs.append((stuff.id, stuff.stuff_type, stuff.name))

    bag_stuffs_list.sort(key=lambda item: item[1:])

    # 更新背包位置
    bag_stuff_position_list = []
    for index, bag_stuff in enumerate(bag_stuffs):
        bag_stuff_position_list.append((bag_stuff, index + 1))

    player_stuff_record.update_bag_stuffs_position(stuff_position_list=bag_stuff_position_list)
