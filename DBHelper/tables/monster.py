from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

Base = declarative_base()

from ..session import session



# 怪物
class Monster(Base):
    """
    怪物
    """
    __tablename__ = 'monster'

    id = Column(Integer, primary_key=True, comment='ID')
    difficulty = Column(Integer, comment='难度值')
    name = Column(Integer, comment='名称')
    exp_value = Column(Integer, comment='被击败后掉落的经验值')

    weekday = Column(String, comment="周几会出现")
    monthday = Column(String, comment="每个月几号会出现")

    attack_property_id = Column(Integer, comment="参考攻击属性")

    active_skill_id = Column(Integer, comment='主动技能名称')

    description = Column(String, comment='怪物说明或者背景')
    drop_stuffs = Column(String, comment='可以掉落的物品')  # 格式为【物品id,概率】的文字列表；


# 增
def add_monster(difficulty: int, name: str, exp_value: int, weekday: str, monthday: str, attack_property_id: int,
                active_skill_id: int, description: str, drop_stuffs: str) -> Monster:
    """
    新增怪物记录

    :param difficulty: 难度值
    :param name: 名称
    :param exp_value: 被击败后掉落的经验值
    :param weekday: 被击败后掉落的经验值
    :param monthday: 被击败后掉落的经验值

    :param attack_property_id: 参考攻击属性
    :param active_skill_id: 主动技能名称
    :param description: 怪物说明或者背景
    :param drop_stuffs: 可以掉落的物品
    :return: None
    """
    monster = Monster(difficulty=difficulty,
                      name=name,
                      exp_value=exp_value,
                      attack_property_id=attack_property_id,
                      weekday=weekday,
                      monthday=monthday,
                      active_skill_id=active_skill_id,
                      description=description,
                      drop_stuffs=drop_stuffs
                      )
    session.add(monster)
    session.commit()
    return monster


# 删
def delete_monster(monster_id: int) -> None:
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
def update_monster(monster_id: int, difficulty: int, name: str, exp_value: int, weekday: str, monthday: str,
                   attack_property_id: int,
                   active_skill_id: int, description: str, drop_stuffs: str):
    """
    修改怪物

    :param monster_id: 怪物ID
    :param difficulty: 难度值
    :param name: 名称
    :param exp_value: 被击败后掉落的经验值

    :param weekday: 在周几会出现
    :param monthday: 在几号会出现

    :param attack_property_id: 参考攻击属性ID
    :param active_skill_id: 主动技能ID
    :param description: 怪物说明或者背景
    :param drop_stuffs: 可以掉落的物品
    :return: None
    """
    monster = session.query(Monster).filter(Monster.id == monster_id).first()
    monster.difficulty = difficulty
    monster.name = name
    monster.exp_value = exp_value
    monster.attack_property_id = attack_property_id
    monster.active_skill_id = active_skill_id
    monster.description = description
    monster.drop_stuffs = drop_stuffs
    session.commit()


# 查
def get_monster_by_id(id: int):
    """
    根据ID查询怪物

    :param session: 数据库会话
    :param id: 怪物ID
    :return: 查询结果
    """
    return session.query(Monster).filter(Monster.id == id).one_or_none()
