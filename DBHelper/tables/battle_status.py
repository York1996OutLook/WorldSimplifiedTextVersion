from typing import List

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from DBHelper.session import session
from Enums import StatusType

Base = declarative_base()


class BattleStatus(Base):
    """
    战斗中的属性，比如中毒，火烧等等；
    """
    __tablename__ = "battle_status"

    id = Column(Integer, primary_key=True)
    name = Column(String, comment="名称")
    status_type = Column(Integer, comment="状态类型")
    effect_expression = Column(String, comment="效果介绍")


# 增
def add(*,
        name: str,
        status_type: int = StatusType.default.index,
        effect_expression: str = ""
        ) -> BattleStatus:
    """
    新增战斗状态
    :param name:
    :param status_type:
    :param effect_expression:
    :return:
    """
    new_status = BattleStatus(name=name, status_type=status_type, effect_expression=effect_expression)
    session.add(new_status)
    session.commit()
    return new_status


# 删
def delete(*,
           battle_status_id: int
           ) -> BattleStatus:
    battle_status = session.query(BattleStatus).filter(BattleStatus.id == battle_status_id).first()
    session.delete(battle_status)
    session.commit()
    return battle_status


# 改
def update(*, battle_status_id: int, name: str = None, status_type=None, effect_expression: str = None) -> BattleStatus:
    """
    Update a BattleStatus record in the database.

    Args:
    - session: A SQLAlchemy session object.
    - id: The id of the BattleStatus record to update.
    - name: The new name for the BattleStatus.
    - status_type:
    - effect_expression: The new effect_expression for the BattleStatus.

    Returns:
    None
    """
    battle_status = session.query(BattleStatus).filter_by(id=battle_status_id).first()
    if name:
        battle_status.name = name
    if status_type:
        battle_status.status_type = status_type
    if effect_expression:
        battle_status.effect_expression = effect_expression

    session.commit()
    return battle_status


def update_by_id(*,
                 battle_status_id: int,
                 name: str = None,
                 status_type: StatusType = None,
                 effect_expression: str = None
                 ) -> BattleStatus:
    """
    Update a BattleStatus record in the database.

    Args:
    - session: A SQLAlchemy session object.
    - id: The id of the BattleStatus record to update.
    - name: The new name for the BattleStatus.
    - status_type:
    - effect_expression: The new effect_expression for the BattleStatus.

    Returns:
    None
    """
    record = update(battle_status_id=battle_status_id, name=name, status_type=status_type,
                    effect_expression=effect_expression)
    return record


# 查

def get_all() -> List[BattleStatus]:
    """
    获取所有的 BattleStatus 信息
    :return: List[BattleStatus]
    """
    return session.query(BattleStatus).all()


def get_by_id(*, status_id: int) -> BattleStatus:
    """
    通过 id 获取 BattleStatus 信息
    :param status_id: BattleStatus 的 id
    :return: BattleStatus
    """
    record = session.query(BattleStatus).filter(BattleStatus.id == status_id).first()
    return record


def get_by_name(*,
                name: str
                ) -> BattleStatus:
    """
    通过名称获取 BattleStatus 信息
    :param name: BattleStatus 的名称
    :return: BattleStatus
    """
    record = session.query(BattleStatus).filter(BattleStatus.name == name).first()
    return record


def is_exists_by_name(*,
                      name: str
                      ) -> bool:
    """
    通过名称获取 BattleStatus 信息
    :param name: BattleStatus 的名称
    :return: BattleStatus
    """
    record = session.query(BattleStatus).filter(BattleStatus.name == name).first()
    return record is not None
