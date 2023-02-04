from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List
from typing import Optional

from worldDB import BasePropertyAddRecord

engine = create_engine("数据库连接字符串")
Session = sessionmaker(bind=engine)
session = Session()


def query_property_add_record_by_player_id(player_id: int) -> List[BasePropertyAddRecord]:
    """
    通过玩家ID查询所有附加属性提升记录
    :param player_id: 玩家ID
    :return: 玩家的所有附加属性提升记录
    """
    return session.query(BasePropertyAddRecord).filter(BasePropertyAddRecord.player_id == player_id).all()

def add_property_add_record(record: BasePropertyAddRecord):
    """
    添加附加属性提升记录
    :param record: 附加属性提升记录
    :return: None
    """
    session.add(record)
    session.commit()

def delete_property_add_record_by_id(record_id: int):
    """
    通过附加属性提升记录ID删除记录
    :param record_id: 附加属性提升记录ID
    :return: None
    """
    session.query(BasePropertyAddRecord).filter(BasePropertyAddRecord.id == record_id).delete()
    session.commit()


def get_base_property_add_record_by_player_id(session: Session, player_id: int) -> List[BasePropertyAddRecord]:
    """
    根据玩家ID查询该玩家的基础属性提升记录
    :param session: sqlalchemy会话
    :param player_id: 玩家ID
    :return: 该玩家的基础属性提升记录列表
    """

    return session.query(BasePropertyAddRecord).filter_by(player_id=player_id).all()