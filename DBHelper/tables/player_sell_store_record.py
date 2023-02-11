from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

Base = declarative_base()
from DBHelper.session import session


# 交易所记录
class PlayerSellStoreRecord(Base):
    __tablename__ = 'player_sell_store_record'

    id = Column(Integer, primary_key=True)

    owner_character_id = Column(Integer, comment="参考player表")

    stuff_record_id = Column(Integer,comment="物品记录ID")

    original_price = Column(Integer, comment='原始售价')
    initial_sell_timestamp = Column(Integer, comment='初始挂售时间')

    is_sold = Column(Boolean, comment="是否被购买")
    deal_timestamp = Column(Integer, comment='交易成交时间')

    tax_rate = Column(Float, comment='税率')
    taxed_price = Column(Float, comment='加税后价格；不足1则按照1进行计算')


# 增
def add_sell_store_record(owner_character_id: int, stuff_name: str, stuff_count: int, original_price: int,
                          initial_sell_timestamp: int, tax_rate: float) -> PlayerSellStoreRecord:
    """
    增加一条交易所记录

    Args:
        owner_character_id (int): 拥有者玩家ID
        stuff_name (str): 物品名称
        stuff_count (int): 物品数量
        original_price (int): 原始售价
        initial_sell_timestamp (int): 初始挂售时间
        tax_rate (float): 税率
    """
    taxed_price = original_price * (1 + tax_rate)
    new_record = PlayerSellStoreRecord(owner_character_id=owner_character_id, stuff_name=stuff_name,
                                       stuff_count=stuff_count,
                                       original_price=original_price, initial_sell_timestamp=initial_sell_timestamp,
                                       is_sold=False, deal_timestamp=None, tax_rate=tax_rate, taxed_price=taxed_price)
    session.add(new_record)
    session.commit()
    return PlayerSellStoreRecord


# 删除
def delete_sell_store_record(*,sell_store_record_id: int):
    """
    删除一条交易所记录

    Args:
        sell_store_record_id (int): 记录的ID
    """
    record = session.query(PlayerSellStoreRecord).get(sell_store_record_id)
    session.delete(record)
    session.commit()


# 改
def update_sell_store_record(record_id: int, new_owner_character_id: int = None, new_stuff_name: str = None,
                             new_stuff_count: int = None, new_original_price: int = None,
                             new_initial_sell_timestamp: int = None, new_tax_rate: float = None):
    """
    修改交易所记录

    Args:
        record_id (int): 记录的ID
        new_owner_character_id (int, optional): 新的拥有者玩家ID
        new_stuff_name (str, optional): 新的物品名称
        new_stuff_count (int, optional): 新的物品数量
        new_original_price (int, optional): 新的原始售价
        new_initial_sell_timestamp (int, optional): 新的初始挂售时间
        new_tax_rate (float, optional): 新的税率
    """
    record = session.query(PlayerSellStoreRecord).get(record_id)
    if new_owner_character_id:
        record.owner_character_id = new_owner_character_id
    if new_stuff_name:
        record.stuff_name = new_stuff_name
    if new_stuff_count:
        record.stuff_count = new_stuff_count
    if new_original_price:
        record.original_price = new_original_price
    if new_initial_sell_timestamp:
        record.initial_sell_timestamp = new_initial_sell_timestamp
    if new_tax_rate:
        record.tax_rate = new_tax_rate
    session.commit()


# 查




def query_sell_store_records(owner_character_id: int = None, stuff_name: str = None, is_sold: bool = None):
    """
    查询交易所记录

    Args:
        owner_character_id (int, optional): 拥有者玩家ID
        stuff_name (str, optional): 物品名称
        is_sold (bool, optional): 是否被购买

    Returns:
        list of SellStoreRecord: 符合条件的记录的列表
    """
    query = session.query(PlayerSellStoreRecord)
    if owner_character_id:
        query = query.filter_by(owner_character_id=owner_character_id)
    if stuff_name:
        query = query.filter_by(stuff_name=stuff_name)
    if is_sold is not None:
        query = query.filter_by(is_sold=is_sold)
    return query.all()


def get_sell_store_record_by_record_id(record_id: int)->PlayerSellStoreRecord:
    """
    根据id查询交易所记录

    Args:
        record_id (int): 记录的ID

    Returns:
        SellStoreRecord: 符合条件的记录
    """
    return session.query(PlayerSellStoreRecord).filter_by(id=record_id).first()


def get_all_sell_store_records_by_timestamp(start_timestamp: int = None, end_timestamp: int = None):
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


def get_expired_records(current_timestamp: int,
                        expired_milliseconds:int
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
