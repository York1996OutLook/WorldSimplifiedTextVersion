from typing import List

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Float, Boolean

from DBHelper.session import session
from DBHelper.tables.base_table import Basic, Base
from DBHelper.tables.base_table import CustomColumn, Timestamp
from Enums import StuffType


class PlayerSellStoreRecord(Basic, Base):
    __cn__ = "交易所"
    __tablename__ = 'player_sell_store_record'
    id = CustomColumn(Integer, cn="ID", primary_key=True, editable=False,autoincrement=True)

    owner_character_id = CustomColumn(Integer, cn="玩家ID", bind_table="Player", comment="参考player表")

    stuff_type = CustomColumn(Integer, cn="物品类型", bind_type=StuffType, comment="物品类型")
    stuff_record_id = CustomColumn(Integer, cn="物品ID", comment="物品记录ID")  # todo

    original_price = CustomColumn(Integer, cn="原始价格", comment='原始售价')
    initial_sell_timestamp = CustomColumn(Timestamp, cn="挂售时间", comment='初始挂售时间')

    is_sold = CustomColumn(Boolean, cn="是否被购买", comment="是否被购买")
    deal_timestamp = CustomColumn(Timestamp, cn="成交时间", comment='交易成交时间')

    taxed_price = CustomColumn(Integer, cn="税后价格", comment='加税后价格;不足1则按照1进行计算')

    @classmethod
    def add_or_update_by_id(cls,
                            *,
                            _id: int = None,
                            owner_character_id: int = None,
                            stuff_type: int = None,
                            stuff_record_id: int = None,
                            original_price: int = None,
                            initial_sell_timestamp: int = None,
                            is_sold: bool = None,
                            deal_timestamp: int = None,
                            tax_rate: float = None,
                            taxed_price: float = None
                            ):
        """
        更新或创建交易记录
        :param _id: 记录ID
        :param owner_character_id: 参考player表
        :param stuff_type: 物品类型
        :param stuff_record_id: 物品记录ID
        :param original_price: 原始售价
        :param initial_sell_timestamp: 初始挂售时间
        :param is_sold: 是否被购买
        :param deal_timestamp: 交易成交时间
        :param tax_rate: 税率
        :param taxed_price: 加税后价格;不足1则按照1进行计算
        :return:
        """
        record = cls._add_or_update_by_id(kwargs=locals())
        return record


def get_all_by_timestamp_range(*,
                               start_timestamp: int = None,
                               end_timestamp: int = None):
    """
    根据时间查询交易所记录

    Args:
        start_timestamp (int, optional): 开始时间，时间戳，以秒为单位
        end_timestamp (int, optional): 结束时间，时间戳，以秒为单位

    Returns:
        list of SellStoreRecord: 符合条件的记录的列表
    """
    query = session.query(PlayerSellStoreRecord)
    if start_timestamp:
        query = query.filter(PlayerSellStoreRecord.initial_sell_timestamp >= start_timestamp)
    if end_timestamp:
        query = query.filter(PlayerSellStoreRecord.initial_sell_timestamp < end_timestamp)
    return query.all()


def get_expired_records(*,
                        current_timestamp: int,
                        expired_milliseconds: int
                        ) -> List[PlayerSellStoreRecord]:
    """

    查询所有已经过期的物品记录

    :param expired_milliseconds: 过期阈值，单位是毫秒
    :param current_timestamp: 目标时间
    :return: 已过期的物品记录列表
    """

    # 查询已过期的物品
    records = session.query(PlayerSellStoreRecord).filter(
        PlayerSellStoreRecord.initial_sell_timestamp < current_timestamp - expired_milliseconds
    )
    return records
