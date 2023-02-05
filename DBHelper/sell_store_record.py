from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

Base = declarative_base()

engine = create_engine("sqlite:///mydatabase.db")
Session = sessionmaker(bind=engine)
session = Session()


# 交易所记录
class SellStoreRecord(Base):
    __tablename__ = 'sell_store_record'

    id = Column(Integer, primary_key=True)

    owner_player_id = Column(Integer, comment="参考")

    stuff_name = Column(String, comment='物品名称')
    stuff_count = Column(Integer, comment="物品个数。如果不可叠加则数量是1，如果可叠加，则数量可以不是1")

    original_price = Column(int, comment='原始售价')
    initial_sell_time = Column(Integer, comment='初始挂售时间')

    is_sold = Column(Boolean, comment="是否被购买")
    deal_time = Column(Integer, comment='交易成交时间')

    tax_rate = Column(Float, comment='税率')
    taxed_price = Column(Float, comment='加税后价格；不足1则按照1进行计算')


# 增
def add_sell_store_record(owner_player_id: int, stuff_name: str, stuff_count: int, original_price: int,
                          initial_sell_time: int, tax_rate: float):
    """
    增加一条交易所记录

    Args:
        owner_player_id (int): 拥有者玩家ID
        stuff_name (str): 物品名称
        stuff_count (int): 物品数量
        original_price (int): 原始售价
        initial_sell_time (int): 初始挂售时间
        tax_rate (float): 税率
    """
    taxed_price = original_price * (1 + tax_rate)
    new_record = SellStoreRecord(owner_player_id=owner_player_id, stuff_name=stuff_name, stuff_count=stuff_count,
                                 original_price=original_price, initial_sell_time=initial_sell_time,
                                 is_sold=False, deal_time=None, tax_rate=tax_rate, taxed_price=taxed_price)
    session.add(new_record)
    session.commit()


# 删除
def delete_sell_store_record(record_id: int):
    """
    删除一条交易所记录

    Args:
        record_id (int): 记录的ID
    """
    record = session.query(SellStoreRecord).get(record_id)
    session.delete(record)
    session.commit()

# 改
def update_sell_store_record(record_id: int, new_owner_player_id: int = None, new_stuff_name: str = None,
                             new_stuff_count: int = None, new_original_price: int = None,
                             new_initial_sell_time: int = None, new_tax_rate: float = None):
    """
    修改交易所记录

    Args:
        record_id (int): 记录的ID
        new_owner_player_id (int, optional): 新的拥有者玩家ID
        new_stuff_name (str, optional): 新的物品名称
        new_stuff_count (int, optional): 新的物品数量
        new_original_price (int, optional): 新的原始售价
        new_initial_sell_time (int, optional): 新的初始挂售时间
        new_tax_rate (float, optional): 新的税率
    """
    record = session.query(SellStoreRecord).get(record_id)
    if new_owner_player_id:
        record.owner_player_id = new_owner_player_id
    if new_stuff_name:
        record.stuff_name = new_stuff_name
    if new_stuff_count:
        record.stuff_count = new_stuff_count
    if new_original_price:
        record.original_price = new_original_price
    if new_initial_sell_time:
        record.initial_sell_time = new_initial_sell_time
    if new_tax_rate:
        record.tax_rate = new_tax_rate
    session.commit()

# 查
def query_sell_store_records(owner_player_id: int = None, stuff_name: str = None, is_sold: bool = None):
    """
    查询交易所记录

    Args:
        owner_player_id (int, optional): 拥有者玩家ID
        stuff_name (str, optional): 物品名称
        is_sold (bool, optional): 是否被购买

    Returns:
        list of SellStoreRecord: 符合条件的记录的列表
    """
    query = session.query(SellStoreRecord)
    if owner_player_id:
        query = query.filter_by(owner_player_id=owner_player_id)
    if stuff_name:
        query = query.filter_by(stuff_name=stuff_name)
    if is_sold is not None:
        query = query.filter_by(is_sold=is_sold)
    return query.all()

def get_sell_store_record_by_id(session, record_id: int):
    """
    根据id查询交易所记录

    Args:
        session (sqlalchemy.orm.session.Session): 数据库会话
        record_id (int): 记录的ID

    Returns:
        SellStoreRecord: 符合条件的记录
    """
    return session.query(SellStoreRecord).filter_by(id=record_id).first()


def query_sell_store_records_by_time(session, start_time: int = None, end_time: int = None):
    """
    根据时间查询交易所记录

    Args:
        session (sqlalchemy.orm.session.Session): 数据库会话
        start_time (int, optional): 起始时间
        end_time (int, optional): 结束时间

    Returns:
        list of SellStoreRecord: 符合条件的记录的列表
    """
    query = session.query(SellStoreRecord)
    if start_time:
        query = query.filter(SellStoreRecord.initial_sell_time >= start_time)
    if end_time:
        query = query.filter(SellStoreRecord.initial_sell_time <= end_time)
    return query.all()
