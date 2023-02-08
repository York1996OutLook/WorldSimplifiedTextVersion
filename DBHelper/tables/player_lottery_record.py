from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

from typing import Optional, List

Base = declarative_base()

from ..session import session


class PlayerLotteryRecord(Base):
    """
    玩家抽奖记录表
    """
    __tablename__ = 'player_lottery_record'

    id = Column(Integer, primary_key=True, comment='抽奖记录ID')

    character_id = Column(Integer, comment="角色ID")

    lottery_num = Column(Integer, comment="抽奖获得的数字；")
    lottery_timestamp = Column(Integer, comment="最后一次抽奖的时间戳；")

    lucky_num = Column(Integer, comment="当天设置的幸运数字")
