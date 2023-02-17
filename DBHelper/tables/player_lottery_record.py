from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, desc

from typing import Optional, List

Base = declarative_base()

from DBHelper.session import session


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


# 增
def add(*, character_id: int,
                              lottery_num: int,
                              lottery_timestamp: int,
                              lucky_num: int
                              ) -> PlayerLotteryRecord:
    """
    新增玩家抽奖记录
    :param character_id: 角色ID
    :param lottery_num: 抽奖获得的数字
    :param lottery_timestamp: 最后一次抽奖的时间戳
    :param lucky_num: 当天设置的幸运数字
    :return: None
    """
    record = PlayerLotteryRecord(
        character_id=character_id,
        lottery_num=lottery_num,
        lottery_timestamp=lottery_timestamp,
        lucky_num=lucky_num
    )
    session.add(record)
    session.commit()
    return record


# 删
def delete(*, record_id: int):
    """
    删除玩家抽奖记录
    :param record_id: 记录ID
    :return: None
    """
    record = session.query(PlayerLotteryRecord).filter_by(id=record_id).first()
    session.delete(record)
    session.commit()


# 改
def update(*, record_id: int, lottery_num: int, lottery_timestamp: int,
                                 lucky_num: int) -> PlayerLotteryRecord:
    """
    修改玩家抽奖记录
    :param record_id: 记录ID
    :param lottery_num: 抽奖获得的数字
    :param lottery_timestamp: 最后一次抽奖的时间戳
    :param lucky_num: 当天设置的幸运数字
    :return: PlayerLotteryRecord
    """
    record = session.query(PlayerLotteryRecord).filter_by(id=record_id).first()
    record.lottery_num = lottery_num
    record.lottery_timestamp = lottery_timestamp
    record.lucky_num = lucky_num
    session.commit()
    session.refresh(record)
    return record


# 查
def get_all_by_timestamp_range(
        *,
        start_timestamp: int,
        end_timestamp: int
) -> List[PlayerLotteryRecord]:
    """
    根据起止时间查询玩家抽奖记录
    :param start_timestamp: 起始时间戳
    :param end_timestamp: 终止时间戳
    :return: 查询结果列表
    """
    records = session.query(PlayerLotteryRecord).filter(PlayerLotteryRecord.lottery_timestamp >= start_timestamp,
                                                        PlayerLotteryRecord.lottery_timestamp <= end_timestamp).all()
    return records


def get_all_is_lucky_num_records_by_timestamp_range(
        *,
        start_timestamp: int,
        end_timestamp: int
) -> List[PlayerLotteryRecord]:
    """
    根据起止时间和幸运数字查询玩家抽奖记录
    :param start_timestamp: 起始时间戳
    :param end_timestamp: 终止时间戳
    :return: 查询结果列表
    """
    records = session.query(PlayerLotteryRecord).filter(PlayerLotteryRecord.lottery_timestamp >= start_timestamp,
                                                        PlayerLotteryRecord.lottery_timestamp <= end_timestamp,
                                                        PlayerLotteryRecord.lucky_num == PlayerLotteryRecord.lottery_num).all()
    return records


def get_all_records_with_max_num_by_timestamp_range(
        *,
        start_timestamp: int,
        end_timestamp: int
) -> List[PlayerLotteryRecord]:
    """
    根据起止时间查询最大幸运数字的玩家抽奖记录
    :param start_timestamp: 起始时间戳
    :param end_timestamp: 终止时间戳
    :return: 查询结果列表
    """
    records = session.query(PlayerLotteryRecord).filter(PlayerLotteryRecord.lottery_timestamp >= start_timestamp,
                                                        PlayerLotteryRecord.lottery_timestamp <= end_timestamp).order_by(
        desc(PlayerLotteryRecord.lucky_num)).all()
    return records
