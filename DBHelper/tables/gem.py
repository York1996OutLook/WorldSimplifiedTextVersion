import os.path as osp

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

from DBHelper.session import session
from Enums import AdditionalPropertyType, property_cn_type_dict
import local_setting
from Utils import tools

Base = declarative_base()


class Gem(Base):
    __tablename__ = 'gem'

    id = Column(Integer, primary_key=True)
    name = Column(String, comment="名称")

    additional_property_type = Column(Integer, comment="参考AdditionalPropertyType")
    increase = Column(Integer, comment="+1还是+2，3，4，5等")
    is_bind = Column(Boolean, comment="刚出来的时候是否已经绑定")

    def __init__(self,
                 *,
                 name: str,
                 additional_property_type: int,
                 increase: int,
                 is_bind: bool
                 ):
        self.name = name
        self.additional_property_type = additional_property_type
        self.increase = increase
        self.is_bind = is_bind


# 增
def add_or_update(*,
                  name: str,
                  additional_property_type: int,
                  increase: int,
                  is_bind: bool
                  ) -> Gem:
    if is_exists_by_name(name=name):
        gem = update_by_name(name=name, additional_property_type=additional_property_type, increase=increase,
                             is_bind=is_bind)
    else:
        gem = add(name=name, additional_property_type=additional_property_type, increase=increase, is_bind=is_bind)
    return gem


def add(*, name: str, additional_property_type: int, increase: int, is_bind: bool) -> Gem:
    gem = Gem(name=name, additional_property_type=additional_property_type, increase=increase, is_bind=is_bind)
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
def update_by_name(*, name: str, additional_property_type: AdditionalPropertyType = None, increase: int = None,
                   is_bind: bool = None) -> Gem:
    """

    :param name:
    :param additional_property_type:
    :param increase:
    :param is_bind:
    :return:
    """
    gem = session.query(Gem).filter(Gem.name == name).first()
    if additional_property_type is not None:
        gem.base_property_id = additional_property_type
    if increase is not None:
        gem.increase = increase
    if is_bind is not None:
        gem.is_bind = is_bind
    session.commit()
    session.refresh(gem)
    return gem


# 查
def is_exists_by_name(*, name: str) -> Gem:
    gem = session.query(Gem).filter(Gem.name == name).first()
    return gem is not None


def get_by_name(*, name: str) -> Gem:
    """
    根据ID查询宝石

    Args:
        name (int): 宝石ID

    Returns:
        Gem: 查询到的宝石
    """
    gem = session.query(Gem).filter(name == name).first()
    return gem


def get_by_id(*, _id: int) -> Gem:
    """
    根据ID查询宝石

    Args:
        _id (int): 宝石ID

    Returns:
        Gem: 查询到的宝石
    """
    gem = session.query(Gem).filter_by(id=id).first()
    return gem


def get_by_base_property_id(*, base_property_id: int):
    """
    根据base_property_id查询宝石

    Args:
        base_property_id (int): 参考基础属性表的ID

    Returns:
        Gem: 查询到的宝石
    """
    gem = session.query(Gem).filter_by(base_property_id=base_property_id).first()
    return gem


def get_all_by_increase(*, increase: int):
    """
    根据increase查询宝石

    Args:
        increase (int): +1还是+2，3，4，5等

    Returns:
        List[Gem]: 查询到的宝石列表
    """
    gems = session.query(Gem).filter_by(increase=increase).all()
    return gems


# other
def json2db():
    gem_json_src = osp.join(local_setting.json_data_root, "gem.json")
    gem_dict_list = tools.file2dict_list(src=gem_json_src)
    for gem_dict in gem_dict_list:
        name = gem_dict['名称']
        additional_property_type = property_cn_type_dict[gem_dict['属性名称']]
        increase = gem_dict['增加属性值']
        is_bind = gem_dict['是否绑定']
        add_or_update(name=name,
                      additional_property_type=additional_property_type,
                      increase=increase,
                      is_bind=is_bind)


if __name__ == '__main__':
    json2db()
