

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
def add_monster(*,difficulty: int, name: str, exp_value: int, description: str, ) -> Monster:
    """
    新增怪物记录

    :param difficulty: 难度值
    :param name: 名称
    :param exp_value: 被击败后掉落的经验值
    :param weekdays: 被击败后掉落的经验值
    :param monthdays: 被击败后掉落的经验值

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
                      weekdays=weekdays,
                      monthdays=monthdays,
                      active_skill_id=active_skill_id,
                      description=description,
                      drop_stuffs=drop_stuffs
                      )
    session.add(monster)
    session.commit()
    return monster


# 删
def delete_monster(*,monster_id: int) -> None:
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
def update_monster(*,monster_id: int, difficulty: int, name: str, exp_value: int, weekday: str, monthday: str,
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
def get_monster_by_id(*,id: int):
    """
    根据ID查询怪物

    :param session: 数据库会话
    :param id: 怪物ID
    :return: 查询结果
    """
    return session.query(Monster).filter(Monster.id == id).one_or_none()


if __name__ == '__main__':
    # insert records into Monster table
    monster1 = Monster(difficulty=5, name='史莱姆', exp_value=200, weekdays='星期二', monthdays='1号', special_days='情人节',
                       description='一种蓝色的生物，常常出没于森林深处。')
    monster2 = Monster(difficulty=7, name='食人魔', exp_value=350, weekdays='星期四', monthdays='5号', special_days='圣诞节',
                       description='一种行动迅速，残忍无情的生物，喜欢吃掉无助的旅行者。')
    monster3 = Monster(difficulty=8, name='龙', exp_value=450, weekdays='星期六', monthdays='10号', special_days='新年',
                       description='一种以智慧和力量著称的生物，生活在高山和岩石间。')

    session.add_all([monster1, monster2, monster3])
    session.commit()
