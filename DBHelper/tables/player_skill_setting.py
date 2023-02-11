from typing import List, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

from Enums import BeingType

Base = declarative_base()

from DBHelper.session import session


class PlayerOrMonsterSkillSetting(Base):
    """
    用户设置的技能释放顺序，每回合只能设置一个主动技能
    """
    __tablename__ = 'player_skill_setting'

    id = Column(Integer, primary_key=True)
    being_type = Column(Integer, comment="参考枚举类型，being_type")
    character_or_monster_id = Column(Integer, comment="character_id or monster_id")  # 参考人物表

    round_index=Column(Integer,comment="第n回合要释放的技能id")
    round_skill=Column(Integer,comment="第n回合要释放的技能id")

    setting_timestamp = Column(Integer, comment="技能设置的时间戳")
