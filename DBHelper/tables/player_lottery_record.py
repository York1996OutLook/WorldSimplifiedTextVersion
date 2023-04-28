from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, desc

from typing import Optional, List


from DBHelper.session import session
from DBHelper.tables.base_table import Basic,Base


class PlayerLotteryRecord(Basic,Base):
    """
    玩家抽奖记录表
    """
    __tablename__ = 'player_lottery_record'

    character_id = Column(Integer, comment="角色ID")

    lottery_num = Column(Integer, comment="抽奖获得的数字;")
    lottery_timestamp = Column(Integer, comment="最后一次抽奖的时间戳;")

    lucky_num = Column(Integer, comment="当天设置的幸运数字")

    @classmethod
    def add_or_update_by_id(cls, *,
                       _id: int,
                       character_id: int = None,
                       lottery_num: int = None,
                       lottery_timestamp: int = None,
                       lucky_num: int = None
                       ):
        """
        更新或创建抽奖记录
        :param _id: 记录ID
        :param character_id: 角色ID
        :param lottery_num: 抽奖获得的数字
        :param lottery_timestamp: 最后一次抽奖的时间戳
        :param lucky_num: 当天设置的幸运数字
        :return:
        """
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
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
