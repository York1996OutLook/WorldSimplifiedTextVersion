import time
from typing import List, Optional



from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean
from DBHelper.tables.player_skill_record import PlayerSkillRecord, \
    get_player_skill_record_by_character_id_and_skill_id, add_player_skill_record, \
    delete_learned_skill_record_bt_skill_record_id
from DBHelper.tables.skill_cost_point import get_kill_point_by_level
from DBHelper.tables.skill_book import get_skill_book_by_skill_id_skill_level, get_skill_id_by_skill_book_id, \
    get_skill_book_by_skill_book_id
from DBHelper.tables.player_skill_record import update_player_skill_record_level_by_character_id, \
    add_player_skill_record

from Enums import MailType
from Utils.tools import find_smallest_missing

Base = declarative_base()


def learn_skill_from_skill_book(*,character_id: int, skill_book_id: int):
    """
    学习某个新的技能
    """
    # 获取某个技能书的skill_book
    skill_book = get_skill_book_by_skill_book_id(skill_book_id=skill_book_id)

    # 获取某个技能书的技能id
    # skill = get_skill_id_by_skill_book_id(skill_book_id=skill_book_id)
    # 查询该玩家是否学习过改技能
    player_skill_record = get_player_skill_record_by_character_id_and_skill_id(character_id=character_id,
                                                                               skill_id=skill_book.skill_id,
                                                                               )

    if player_skill_record is None:  # 说明没有学习过这个player skill
        add_player_skill_record(character_id=character_id,
                                skill_id=skill_book.skill_id,
                                skill_level=1,
                                learning_timestamp=int(time.time()))
    else:
        # 技能等级+1
        update_player_skill_record_level_by_character_id(record_id=player_skill_record.id,
                                                         skill_level=player_skill_record.skill_level + 1,
                                                         learning_timestamp=int(time.time())
                                                         )


def abandon_skill(*,character_id: int, skill_id: int, abandon_levels: int):
    """
    放弃技能
    """
    # 查询该玩家学过该技能的等级
    player_skill_record = get_player_skill_record_by_character_id_and_skill_id(character_id=character_id,
                                                                               skill_id=skill_id,
                                                                               )

    if player_skill_record.skill_level == abandon_levels:  # 技能等级 - n
        delete_learned_skill_record_bt_skill_record_id(player_skill_record.id)
    else:
        # 技能等级 - n
        update_player_skill_record_level_by_character_id(record_id=player_skill_record.id,
                                                         skill_level=player_skill_record.skill_level - abandon_levels,
                                                         learning_timestamp=int(time.time())
                                                         )
    skill_point = 0
    for i in range(player_skill_record.skill_level - abandon_levels, player_skill_record.skill_level + 1):
        skill_point += get_kill_point_by_level(i)

    return skill_point
