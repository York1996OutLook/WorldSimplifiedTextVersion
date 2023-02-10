from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

Base = declarative_base()
from ..session import session



class BattleStatus(Base):
    """
    战斗中的属性，比如中毒，火烧等等；
    """
    __tablename__ = "BattleStatus"

    id = Column(Integer, primary_key=True)
    name = Column(String, comment="名称")
    effect = Column(String, comment="效果")


# 增
def add_battle_status(name: str, effect: str)->BattleStatus:
    """
    新增战斗状态
    :param name:
    :param effect:
    :return:
    """
    new_status = BattleStatus(name=name, effect=effect)
    session.add(new_status)
    session.commit()
    return new_status


# 删
def delete_battle_status(battle_status_id:int):
    battle_status = session.query(BattleStatus).filter(BattleStatus.id == battle_status_id).first()
    if battle_status:
        session.delete(battle_status)
        session.commit()
        print("删除成功")
    else:
        print("记录不存在")


# 改
def update_battle_status(id, name=None, effect=None):
    """
    Update a BattleStatus record in the database.

    Args:
    - session: A SQLAlchemy session object.
    - id: The id of the BattleStatus record to update.
    - name: The new name for the BattleStatus.
    - effect: The new effect for the BattleStatus.

    Returns:
    None
    """
    battle_status = session.query(BattleStatus).filter_by(id=id).first()
    if not battle_status:
        raise ValueError(f"BattleStatus with id {id} not found.")

    if name:
        battle_status.name = name
    if effect:
        battle_status.effect = effect

    session.commit()

# 查

def get_all_battle_statuses():
    """
    获取所有的 BattleStatus 信息
    :return: List[BattleStatus]
    """
    return session.query(BattleStatus).all()


def get_battle_status_by_id(status_id: int):
    """
    通过 id 获取 BattleStatus 信息
    :param status_id: BattleStatus 的 id
    :return: BattleStatus
    """
    return session.query(BattleStatus).filter(BattleStatus.id == status_id).first()


def get_battle_status_by_name(status_name: str):
    """
    通过名称获取 BattleStatus 信息
    :param status_name: BattleStatus 的名称
    :return: BattleStatus
    """
    return session.query(BattleStatus).filter(BattleStatus.name == status_name).first()