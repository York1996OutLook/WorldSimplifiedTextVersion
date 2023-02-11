from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean
from DBHelper.session import session

from Enums import BattleType

Base = declarative_base()


class PlayerBattleRecord(Base):
    """
    战斗中记录表
    """
    __tablename__ = "battle_record"
    id = Column(Integer, primary_key=True)
    battle_type = Column(Integer, comment="战斗类型，参考BattleType")

    positive_character_id = Column(Integer, comment="主动攻击角色ID")
    passive_character_id = Column(Integer, comment="被动攻击角色ID")

    positive_won = Column(Boolean, comment="主动攻击人是否胜利")
    battle_text = Column(String, comment="战斗产生的文字说明")


# 增
def add_battle_record(*, battle_type: int, positive_id: int, passive_id: int, positive_won: bool,
                      battle_text: str) -> PlayerBattleRecord:
    """
    向战斗记录表中添加一条记录

    Args:
    - battle_type (int): 战斗类型
    - positive_id (int): 主动攻击character ID
    - passive_id (int): 被动攻击character ID
    - positive_won (bool): 主动攻击人是否胜利
    - battle_text (str): 战斗产生的文字说明

    Returns:
    - None: 没有返回值

    """
    new_record = PlayerBattleRecord(
        battle_type=battle_type,
        positive_id=positive_id,
        passive_id=passive_id,
        positive_won=positive_won,
        battle_text=battle_text
    )
    session.add(new_record)
    session.commit()
    return new_record


# 删
def delete_battle_record(*, record_id: int) -> None:
    """
    删除战斗记录表中的一条记录

    Args:
    - record_id (int): 要删除的记录的id

    Returns:
    - None: 没有返回值

    """
    record_to_delete = session.query(PlayerBattleRecord).filter(PlayerBattleRecord.id == record_id).first()
    session.delete(record_to_delete)
    session.commit()


# 改
def update_battle_record_won(*, record_id: int, positive_won: bool) -> None:
    """
    修改战斗记录表中的主动攻击是否获胜

    Args:
    - record_id (int): 要修改的记录的id
    - positive_won (bool): 修改后的主动攻击是否获胜

    Returns:
    - None: 没有返回值

    """
    record_to_update = session.query(PlayerBattleRecord).filter(PlayerBattleRecord.id == record_id).first()
    record_to_update.positive_won = positive_won
    session.commit()


def update_battle_record_text(*, record_id: int, battle_text: str) -> None:
    """
    修改战斗记录表中的战斗产生的文字说明

    Args:
    - record_id (int): 要修改的记录的id
    - battle_text (str): 修改后的战斗产生的文字说明

    Returns:
    - None: 没有返回值

    """
    record_to_update = session.query(PlayerBattleRecord).filter(PlayerBattleRecord.id == record_id).first()
    record_to_update.battle_text = battle_text
    session.commit()


def update_battle_record_positive_id(*, record_id: int, positive_character_id: int) -> None:
    """
    修改战斗记录表中的主动攻击characterID

    Args:
    - record_id (int): 要修改的记录的id
    - positive_id (int): 修改后的主动攻击character ID

    Returns:
    - None: 没有返回值

    """
    record_to_update = session.query(PlayerBattleRecord).filter(PlayerBattleRecord.id == record_id).first()
    record_to_update.positive_id = positive_character_id
    session.commit()


# 查询

def get_battles_by_positive_id(*, positive_id:int):
    """
    查询主动攻击者是positive_id的所有战斗记录
    """
    return session.query(PlayerBattleRecord).filter_by(positive_id=positive_id).all()


def get_battles_by_passive_id(*, passive_id:int):
    """
    查询被动攻击者是passive_id的所有战斗记录
    """
    return session.query(PlayerBattleRecord).filter_by(passive_id=passive_id).all()


def get_battles_by_battle_type(*, battle_type: BattleType):
    """
    查询战斗类型为battle_type的所有战斗记录
    """
    return session.query(PlayerBattleRecord).filter_by(battle_type=battle_type).all()


def get_battles_by_result(*, positive_won: bool):
    """
    查询主动攻击者胜利/失败的所有战斗记录
    """
    return session.query(PlayerBattleRecord).filter_by(positive_won=positive_won).all()


def get_all_battles():
    """
    查询所有战斗记录
    """
    return session.query(PlayerBattleRecord).all()
