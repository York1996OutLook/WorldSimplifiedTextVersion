from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from DBHelper.session import session

Base = declarative_base()


class BattleStatus(Base):
    """
    战斗中的属性，比如中毒，火烧等等；
    """
    __tablename__ = "battle_status"

    id = Column(Integer, primary_key=True)
    name = Column(String, comment="名称")
    effect = Column(String, comment="效果")


# 增
def add(*, name: str, effect: str) -> BattleStatus:
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
def delete(*, battle_status_id: int):
    battle_status = session.query(BattleStatus).filter(BattleStatus.id == battle_status_id).first()
    session.delete(battle_status)
    session.commit()


# 改
def update(*, battle_status_id: int, name: str = None, effect: str = None):
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
    battle_status = session.query(BattleStatus).filter_by(id=battle_status_id).first()
    if name:
        battle_status.name = name
    if effect:
        battle_status.effect = effect

    session.commit()


# 查

def get_all():
    """
    获取所有的 BattleStatus 信息
    :return: List[BattleStatus]
    """
    return session.query(BattleStatus).all()


def get_by_id(*, status_id: int):
    """
    通过 id 获取 BattleStatus 信息
    :param status_id: BattleStatus 的 id
    :return: BattleStatus
    """
    return session.query(BattleStatus).filter(BattleStatus.id == status_id).first()


def get_by_name(*, name: str):
    """
    通过名称获取 BattleStatus 信息
    :param name: BattleStatus 的名称
    :return: BattleStatus
    """
    return session.query(BattleStatus).filter(BattleStatus.name == name).first()


if __name__ == '__main__':
    # 假设名称和效果已经定义好
    status_names = ["中毒", "火烧", "冰冻", "沉默", "昏睡"]
    status_effects = ["生命值每回合减少5%", "受到的伤害增加25%", "出手速度减少50%", "无法使用技能", "回合数+1"]

    # 插入数据
    for status_name, status_effect in zip(status_names, status_effects):
        new_record = BattleStatus(name=status_name, effect=status_effect)
        session.add(new_record)

    session.commit()
