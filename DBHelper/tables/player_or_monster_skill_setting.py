import time
from typing import List, Optional

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

from DBHelper.session import session
from DBHelper.tables.base_table import Basic,Base
from Enums import BeingType



class PlayerOrMonsterSkillSetting(Basic,Base):
    """
    用户设置的技能释放顺序,每回合只能设置一个主动技能
    """
    __tablename__ = 'player_or_monster_skill_setting'

    being_type = Column(Integer, comment="参考枚举类型,being_type")
    character_or_monster_id = Column(Integer, comment="character_id or monster_id")  # 参考人物表

    round_index = Column(Integer, comment="第n回合,从1开始")
    skill_book_id = Column(Integer, comment="技能书,其中包含了技能名称和技能等级")

    setting_timestamp = Column(Integer, comment="技能设置的时间戳")

    @classmethod
    def add_or_update_by_id(cls, *,
                       _id: int,
                       being_type: int = None,
                       character_or_monster_id: int = None,
                       round_index: int = None,
                       skill_book_id: int = None,
                       setting_timestamp: int = None
                       ):
        """
        更新或创建技能设置记录
        :param _id: 记录ID
        :param being_type: 参考枚举类型,being_type
        :param character_or_monster_id: character_id or monster_id
        :param round_index: 第n回合,从1开始
        :param skill_book_id: 技能书,其中包含了技能名称和技能等级
        :param setting_timestamp: 技能设置的时间戳
        :return:
        """
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
        return record


def add_monster_skill_setting(*,
                              monster_id: int,
                              round_index: int,
                              skill_book_id: int, ):
    add(being_type=BeingType.MONSTER,
        character_or_monster_id=monster_id,
        round_index=round_index,
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
