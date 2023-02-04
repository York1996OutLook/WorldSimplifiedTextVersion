from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from worldDB import BattleStatus

engine = create_engine("sqlite:///mydatabase.db")
Session = sessionmaker(bind=engine)
session = Session()



# 增

# 删

# 改


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
