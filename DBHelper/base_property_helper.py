from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List
from typing import Optional

from worldDB import BaseProperty

engine = create_engine("数据库连接字符串")
Session = sessionmaker(bind=engine)
session = Session()


def get_all_base_properties() -> List[BaseProperty]:
    """
    返回所有基础属性

    Returns:
        List[BaseProperty]: 所有基础属性列表
    """
    return session.query(BaseProperty).all()


def get_base_property_by_id(property_id: int) -> Optional[BaseProperty]:
    """
    根据id查询基础属性

    Args:
        property_id (int): 属性id

    Returns:
        Optional[BaseProperty]: 基础属性，如果不存在则返回None
    """
    return session.query(BaseProperty).filter_by(id=property_id).first()


def get_base_property_by_name(property_name: str) -> Optional[BaseProperty]:
    """
    根据名字查询基础属性

    Args:
        property_name (str): 属性名字

    Returns:
        Optional[BaseProperty]: 基础属性，如果不存在则返回None
    """
    return session.query(BaseProperty).filter_by(name=property_name).first()


def add_base_property(property_name: str) -> BaseProperty:
    """
    新增基础属性

    Args:
        property_name (str): 属性名字

    Returns:
        BaseProperty: 新增的基础属性
    """
    new_property = BaseProperty(name=property_name)
    session.add(new_property)
    session.commit()
    return new_property


def update_base_property(property_id: int, new_property_name: str) -> BaseProperty:
    """
    更新基础属性

    Args:
        property_id (int): 属性id
        new_property_name (str): 新的属性名字

    Returns:
        BaseProperty: 更新后的基础属性
    """
    property = session.query(BaseProperty).filter_by(id=property_id).first()
    if property:
        property.name = new_property_name
        session.commit()
    return property

def delete_base_property(property_id: int) -> bool:
    """
    删除基础属性
    Args:
        property_id(int): 属性id

    Returns:
    bool: 删除是否成功
    """
    property = session.query(BaseProperty).filter_by(id=property_id).first()
    if property:
        session.delete(property)
        session.commit()
        return True
    else:
        return False


