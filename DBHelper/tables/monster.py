from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

Base = declarative_base()

from DBHelper.session import session


# 怪物
class Monster(Base):
    """
    怪物
    """
    __tablename__ = 'monster'

    id = Column(Integer, primary_key=True, comment='ID')
    name = Column(Integer, comment='名称')

    exp_value = Column(Integer, comment='被击败后掉落的经验值')
    description = Column(String, comment='怪物说明或者背景')


# 增
def add_monster(*, name: str, exp_value: int, description: str, ) -> Monster:
    """
    新增怪物记录

    :param name: 名称
    :param exp_value: 被击败后掉落的经验值
    :param description: 怪物说明或者背景
    :return: None
    """
    monster = Monster(
        name=name,
        exp_value=exp_value,
        description=description,
    )
    session.add(monster)
    session.commit()
    return monster


# 删
def delete_monster(*, monster_id: int) -> None:
    """
    删除怪物信息

    :param monster_id: 要删除的怪物ID
    :return: None
    """
    monster = session.query(Monster).filter(Monster.id == monster_id).first()
    if monster:
        session.delete(monster)
        session.commit()


# 改
def update_monster(*,
                   monster_id: int,
                   name: str,
                   exp_value: int,
                   description: str, ):
    """
    修改怪物

    :param monster_id: 怪物ID
    :param name: 名称
    :param exp_value: 被击败后掉落的经验值

    :param description: 怪物说明或者背景
    :return: None
    """
    monster = session.query(Monster).filter(Monster.id == monster_id).first()
    monster.name = name
    monster.exp_value = exp_value
    monster.description = description
    session.commit()


# 查
def get_monster_by_id(*, monster_id: int):
    """
    根据ID查询怪物

    :param monster_id: 怪物ID
    :return: 查询结果
    """
    return session.query(Monster).filter(Monster.id == monster_id).one_or_none()


