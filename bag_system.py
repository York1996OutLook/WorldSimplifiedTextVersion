import time
from collections import defaultdict, OrderedDict
from typing import List

from sqlalchemy import Boolean

from DBHelper.tables.player_achievement_record import get_all_achievements_records_by_character_id
from DBHelper.tables.achievement import get_achievement_by_achievement_id
from DBHelper.tables.skill_achievement_equipment_etc_properties import SkillAchievementEquipmentEtcProperties, \
    get_properties_dict_by_source_type_and_id
from DBHelper.tables.player_skill_record import PlayerSkillRecord, \
    get_player_skill_record_by_character_id_and_skill_id
from DBHelper.tables.skill_book import SkillBook, get_skill_book_by_skill_id_skill_level
from DBHelper.tables.player_stuff_record import PlayerStuffRecord, get_all_wearing_stuffs_by_character_id, \
    get_all_in_bag_stuffs_by_character_id
from DBHelper.tables.equipment_gem_record import get_all_gems_by_equipment_id
from DBHelper.tables.gem import get_gem_by_gem_id
from DBHelper.tables.setting import get_per_star_improved_percent, get_sell_expire_hours, get_game_master_id
from DBHelper.tables.setting import get_lottery_start_hour, get_lottery_end_hour, get_lottery_lucky_num
from DBHelper.tables.player_lottery_record import get_all_is_lucky_num_player_lottery_records_by_timestamp
from DBHelper.tables.player_lottery_record import get_all_player_lottery_records_with_max_lucky_num_by_timestamp
from DBHelper.tables.player_mail_record import insert_player_mail_record_to_available_position
from DBHelper.tables.player_stuff_record import get_player_stuff_record_by_record_id, add_player_stuff_record, \
    insert_stuff_to_player_bag
from DBHelper.tables.player_sell_store_record import get_sell_store_record_by_record_id, get_expired_records, \
    delete_sell_store_record
from DBHelper.tables.stuff import get_stuff_by_stuff_id
from mail_system import send_email

from Enums import AdditionSourceType, AdditionalPropertyType, BasePropertyType, MailType
from Utils import tools

from DBHelper.session import session


def player_sort_bag(character_id: int):
    """
    对玩家的背包进行排序，重新安排背包中物品的位置；
    :param character_id:
    :return:
    """
    bag_stuffs = get_all_in_bag_stuffs_by_character_id(character_id=character_id)

    # order by stuff.type stuff.name
    bag_stuffs_list = []
    for bag_stuff in bag_stuffs:
        stuff = get_stuff_by_stuff_id(bag_stuff.stuff_id)
        bag_stuffs.append((stuff.id, stuff.stuff_type, stuff.name))

    bag_stuffs_list.sort(key=lambda item: item[1:])

    for index, bag_stuff in enumerate(bag_stuffs):
        bag_stuff.position_in_bag = index + 1  # +1 的原因是这里enumerate返回的索引是从0开始的，而背包的位置是从1开始的。

    session.commit()
