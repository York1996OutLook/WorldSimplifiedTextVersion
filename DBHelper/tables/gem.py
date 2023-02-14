from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

from DBHelper.session import session

from Enums import AdditionalPropertyType

Base = declarative_base()


class Gem(Base):
    __tablename__ = 'gem'

    id = Column(Integer, primary_key=True)
    additional_property_type = Column(Integer, comment="参考AdditionalPropertyType")
    increase = Column(Integer, comment="+1还是+2，3，4，5等")

    is_bind = Column(Boolean, comment="刚出来的时候是否已经绑定")


# 增
def add_gem(*, base_property_id: int, increase: int) -> Gem:
    """
    新增宝石

    Args:
        base_property_id (int): 参考基础属性表的ID
        increase (int): 增加的数值

    Returns:
        Gem: 新增的宝石
    """
    gem = Gem(base_property_id=base_property_id, increase=increase)
    session.add(gem)
    session.commit()
    return gem


# 删
def delete_gem(*, gem_id: int):
    """
    删除宝石

    Args:
        gem_id (int): 宝石ID

    Returns:
        bool: 是否删除成功
    """
    gem = session.query(Gem).filter_by(id=gem_id).first()
    session.delete(gem)
    session.commit()
    return True


# 改
def update_gem(*, gem_id: int, base_property_id: int = None, increase: int = None):
    """
    修改宝石

    Args:
        gem_id (int): 宝石ID
        base_property_id (int, optional): 参考基础属性表的ID. Defaults to None.
        increase (int, optional): 增加的数值. Defaults to None.

    Returns:
        Gem: 修改后的宝石
    """
    gem = session.query(Gem).filter_by(id=gem_id).first()
    if base_property_id is not None:
        gem.base_property_id = base_property_id
    if increase is not None:
        gem.increase = increase
    session.commit()
    return gem


# 查
def get_gem_by_gem_id(*, gem_id: int) -> Gem:
    """
    根据ID查询宝石

    Args:
        gem_id (int): 宝石ID

    Returns:
        Gem: 查询到的宝石
    """
    gem = session.query(Gem).filter_by(id=gem_id).first()
    return gem


def get_gem_by_base_property_id(*, base_property_id: int):
    """
    根据base_property_id查询宝石

    Args:
        base_property_id (int): 参考基础属性表的ID

    Returns:
        Gem: 查询到的宝石
    """
    gem = session.query(Gem).filter_by(base_property_id=base_property_id).first()
    return gem


def get_gems_by_increase(*, increase: int):
    """
    根据increase查询宝石

    Args:
        increase (int): +1还是+2，3，4，5等

    Returns:
        List[Gem]: 查询到的宝石列表
    """
    gems = session.query(Gem).filter_by(increase=increase).all()
    return gems


if __name__ == '__main__':
    gem_list = [
        Gem(additional_property_type=AdditionalPropertyType.PHYSIQUE, increase=1, is_bind=False),
        Gem(additional_property_type=AdditionalPropertyType.PHYSIQUE, increase=2, is_bind=False),
        Gem(additional_property_type=AdditionalPropertyType.PHYSIQUE, increase=3, is_bind=False),
        Gem(additional_property_type=AdditionalPropertyType.PHYSIQUE, increase=4, is_bind=False),
        Gem(additional_property_type=AdditionalPropertyType.PHYSIQUE, increase=5, is_bind=False),

        Gem(additional_property_type=AdditionalPropertyType.STRENGTH, increase=1, is_bind=False),
        Gem(additional_property_type=AdditionalPropertyType.STRENGTH, increase=2, is_bind=False),
        Gem(additional_property_type=AdditionalPropertyType.STRENGTH, increase=3, is_bind=False),
        Gem(additional_property_type=AdditionalPropertyType.STRENGTH, increase=4, is_bind=False),
        Gem(additional_property_type=AdditionalPropertyType.STRENGTH, increase=5, is_bind=False),

        Gem(additional_property_type=AdditionalPropertyType.AGILITY, increase=1, is_bind=False),
        Gem(additional_property_type=AdditionalPropertyType.AGILITY, increase=2, is_bind=False),
        Gem(additional_property_type=AdditionalPropertyType.AGILITY, increase=3, is_bind=False),
        Gem(additional_property_type=AdditionalPropertyType.AGILITY, increase=4, is_bind=False),
        Gem(additional_property_type=AdditionalPropertyType.AGILITY, increase=5, is_bind=False),

        Gem(additional_property_type=AdditionalPropertyType.INTELLIGENCE, increase=1, is_bind=False),
        Gem(additional_property_type=AdditionalPropertyType.INTELLIGENCE, increase=2, is_bind=False),
        Gem(additional_property_type=AdditionalPropertyType.INTELLIGENCE, increase=3, is_bind=False),
        Gem(additional_property_type=AdditionalPropertyType.INTELLIGENCE, increase=4, is_bind=False),
        Gem(additional_property_type=AdditionalPropertyType.INTELLIGENCE, increase=5, is_bind=False),

        Gem(additional_property_type=AdditionalPropertyType.PERCEPTION, increase=1, is_bind=False),
        Gem(additional_property_type=AdditionalPropertyType.PERCEPTION, increase=2, is_bind=False),
        Gem(additional_property_type=AdditionalPropertyType.PERCEPTION, increase=3, is_bind=False),
        Gem(additional_property_type=AdditionalPropertyType.PERCEPTION, increase=4, is_bind=False),
        Gem(additional_property_type=AdditionalPropertyType.PERCEPTION, increase=5, is_bind=False),

        Gem(additional_property_type=AdditionalPropertyType.CRITICAL_POINT, increase=1, is_bind=False),
        Gem(additional_property_type=AdditionalPropertyType.CRITICAL_POINT, increase=2, is_bind=False),
        Gem(additional_property_type=AdditionalPropertyType.CRITICAL_POINT, increase=3, is_bind=False),
        Gem(additional_property_type=AdditionalPropertyType.CRITICAL_POINT, increase=4, is_bind=False),
        Gem(additional_property_type=AdditionalPropertyType.CRITICAL_POINT, increase=5, is_bind=False),

        Gem(additional_property_type=AdditionalPropertyType.HEALTH, increase=20, is_bind=False),
        Gem(additional_property_type=AdditionalPropertyType.HEALTH, increase=50, is_bind=False),

        Gem(additional_property_type=AdditionalPropertyType.MANA, increase=20, is_bind=False),
        Gem(additional_property_type=AdditionalPropertyType.MANA, increase=50, is_bind=False),
    ]

    session.add_all(gem_list)
    session.commit()
