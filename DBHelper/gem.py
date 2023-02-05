from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

Base = declarative_base()

engine = create_engine("sqlite:///mydatabase.db")
Session = sessionmaker(bind=engine)
session = Session()


class Gem(Base):
    __tablename__ = 'gem'

    id = Column(Integer, primary_key=True)
    base_property_id = Column(Integer, comment="参考基础属性表，暂时不考虑加入其它属性的宝石")
    increase = Column(Integer, comment="+1还是+2，3，4，5等")


# 增
def add_gem(base_property_id: int, increase: int):
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
def delete_gem(id: int):
    """
    删除宝石

    Args:
        id (int): 宝石ID

    Returns:
        bool: 是否删除成功
    """
    gem = session.query(Gem).filter_by(id=id).first()
    if not gem:
        return False
    session.delete(gem)
    session.commit()
    return True


# 改
def update_gem(gem_id: int, base_property_id: int = None, increase: int = None):
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
    if not gem:
        return None
    if base_property_id is not None:
        gem.base_property_id = base_property_id
    if increase is not None:
        gem.increase = increase
    session.commit()
    return gem


# 查
def get_gem(gem_id: int):
    """
    根据ID查询宝石

    Args:
        gem_id (int): 宝石ID

    Returns:
        Gem: 查询到的宝石
    """
    gem = session.query(Gem).filter_by(id=gem_id).first()
    return gem


def get_gem_by_base_property_id(base_property_id: int):
    """
    根据base_property_id查询宝石

    Args:
        base_property_id (int): 参考基础属性表的ID

    Returns:
        Gem: 查询到的宝石
    """
    gem = session.query(Gem).filter_by(base_property_id=base_property_id).first()
    return gem


def get_gems_by_increase(increase: int):
    """
    根据increase查询宝石

    Args:
        increase (int): +1还是+2，3，4，5等

    Returns:
        List[Gem]: 查询到的宝石列表
    """
    gems = session.query(Gem).filter_by(increase=increase).all()
    return gems
