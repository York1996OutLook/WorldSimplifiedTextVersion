from typing import List, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean
from DBHelper.tables.player_skill_record import PlayerSkillRecord, \
    get_player_skill_record_by_character_id_and_skill_id,add_learned_skill_record
from DBHelper.tables.skill_book import get_skill_book_by_skill_id_skill_level, get_skill_id_by_skill_book_id, \
    get_skill_book_by_skill_book_id

from Enums import EmailType
from Utils.tools import find_smallest_missing

Base = declarative_base()


def learn_skill_from_skill_book(character_id: int, skill_book_id: int):
    """
    学习某个新的技能
    """
    # 获取某个技能书的skill_book
    skill_book = get_skill_book_by_skill_book_id(skill_book_id=skill_book_id)

    # 获取某个技能书的技能id
    # skill = get_skill_id_by_skill_book_id(skill_book_id=skill_book_id)
    # 查询该玩家是否学习过改技能
    player_skill = get_player_skill_record_by_character_id_and_skill_id(character_id=character_id,
                                                                        skill_id = skill_book.skill_id
                                                                        )

    if player_skill is None:    # 说明没有学习过这个player skill
        ...
    else:
        # 判断等级
        add_learned_skill_record(character_id,)
