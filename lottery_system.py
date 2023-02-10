from collections import defaultdict
from typing import List

from DBHelper.tables.player_achievement_record import get_all_achievements_records_by_character_id
from DBHelper.tables.achievement import get_achievement_by_achievement_id
from DBHelper.tables.skill_achievement_equipment_etc_properties import SkillAchievementEquipmentEtcProperties, \
    get_properties_dict_by_source_type_and_id
from DBHelper.tables.player_skill_record import PlayerSkillRecord, \
    get_player_skill_record_by_character_id_and_skill_id
from DBHelper.tables.skill_book import SkillBook, get_skill_book_by_skill_id_skill_level
from DBHelper.tables.player_stuff_record import PlayerStuffRecord, get_all_wearing_stuffs_by_character_id
from DBHelper.tables.equipment_gem_record import get_all_gems_by_equipment_id
from DBHelper.tables.gem import get_gem_by_gem_id
from DBHelper.tables.setting import get_per_star_improved_percent
from DBHelper.tables.setting import get_lottery_start_hour, get_lottery_end_hour, get_lottery_lucky_num
from DBHelper.tables.player_lottery_record import get_all_is_lucky_num_player_lottery_records_by_timestamp
from DBHelper.tables.player_lottery_record import get_all_player_lottery_records_with_max_lucky_num_by_timestamp

from Enums import AdditionSourceType, AdditionalPropertyType, BasePropertyType
from Utils import tools


def get_today_lottery_winners():
    """
    获取
    """
    # 获取今天可以抽奖时间段内的最大号码
    start_hour, end_hour = get_lottery_start_hour(), get_lottery_end_hour()

    today_start_timestamp = tools.get_today_timestamp(start_hour)
    today_end_timestamp = tools.get_today_timestamp(end_hour)

    # 获取当日最大号码的记录
    all_max_num_player_lottery_records = get_all_player_lottery_records_with_max_lucky_num_by_timestamp(
        start_timestamp=today_start_timestamp,
        end_timestamp=today_end_timestamp
    )

    # 获取当日抽的幸运数字的记录
    all_is_lucky_num_player_lottery_records = get_all_is_lucky_num_player_lottery_records_by_timestamp(
        start_timestamp=today_start_timestamp,
        end_timestamp=today_end_timestamp
    )
    
    character_ids = set()
    for record in [*all_max_num_player_lottery_records,*all_is_lucky_num_player_lottery_records]:
        character_ids.add(record.character_id)

    return character_ids
