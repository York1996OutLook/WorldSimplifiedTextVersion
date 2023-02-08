from collections import defaultdict
from typing import List

from DBHelper.tables.player_achievement_record import get_all_achievements_records_by_character_id
from DBHelper.tables.achievement import get_achievement_by_achievement_id
from DBHelper.tables.skill_achievement_equipment_etc_properties import SkillAchievementEquipmentEtcProperties, \
    get_properties_dict_by_source_type_and_id
from DBHelper.tables.player_skill_record import PlayerSkillRecord, \
    get_all_player_skill_records_by_character_id_or_skill_id
from DBHelper.tables.skill_book import SkillBook, get_skill_book_by_skill_id_skill_level
from DBHelper.tables.player_stuff_record import PlayerStuffRecord, get_all_wearing_stuffs_by_character_id
from DBHelper.tables.equipment_gem_record import get_all_gems_by_equipment_id
from DBHelper.tables.gem import get_gem_by_gem_id
from DBHelper.tables.setting import get_per_star_improved_percent
from DBHelper.tables.setting import get_lottery_start_hour,get_lottery_end_hour,get_lottery_lucky_num

from Enums import AdditionSourceType, AdditionalPropertyType, BasePropertyType
from Utils import tools

def get_today_lottery_winners():
    start_hour,end_hour = get_lottery_start_hour(),get_lottery_end_hour()

    # get max num winners
    today_start_timestamp = tools.get_today_timestamp(0)
    today_end_timestamp = tools.get_today_timestamp(0)