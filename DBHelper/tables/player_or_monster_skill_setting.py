import time
from typing import List, Optional

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

from Enums import BeingType

Base = declarative_base()

from DBHelper.session import session


class PlayerOrMonsterSkillSetting(Base):
    """
    用户设置的技能释放顺序，每回合只能设置一个主动技能
    """
    __tablename__ = 'player_or_monster_skill_setting'

    id = Column(Integer, primary_key=True)
    being_type = Column(Integer, comment="参考枚举类型，being_type")
    character_or_monster_id = Column(Integer, comment="character_id or monster_id")  # 参考人物表

    round_index = Column(Integer, comment="第n回合,从1开始")
    skill_book_id = Column(Integer, comment="技能书，其中包含了技能名称和技能等级")

    setting_timestamp = Column(Integer, comment="技能设置的时间戳")

    def __init__(self,
                 *,
                 being_type: BeingType,
                 character_or_monster_id: int,
                 skill_book_id: int,
                 setting_timestamp: int):
        self.being_type = being_type
        self.character_or_monster_id = character_or_monster_id
        self.skill_book_id = skill_book_id
        self.setting_timestamp = setting_timestamp


# 增
def add(*,
        being_type: BeingType,
        character_or_monster_id: int,
        skill_book_id: int,
        setting_timestamp: int):
    setting = PlayerOrMonsterSkillSetting(being_type=being_type,
                                          character_or_monster_id=character_or_monster_id,
                                          skill_book_id=skill_book_id,
                                          setting_timestamp=setting_timestamp)
    return setting


def add_monster_skill_setting(*,
                              monster_id: int,
                              skill_book_id: int, ):
    add(being_type=BeingType.MONSTER,
        character_or_monster_id=monster_id,
        skill_book_id=skill_book_id,
        setting_timestamp=int(time.time())
        )


def add_player_skill_setting(*,
                             player_id: int,
                             skill_book_id: int, ):
    add(being_type=BeingType.PLAYER,
        character_or_monster_id=player_id,
        skill_book_id=skill_book_id,
        setting_timestamp=int(time.time())
        )


# 删
def del_monster_skill_setting(*, monster_id: int):
    session.query(PlayerOrMonsterSkillSetting).filter(
        PlayerOrMonsterSkillSetting.character_or_monster_id == monster_id
    ).delete()
    return True
# 改

# 查
