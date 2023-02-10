from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from typing import List

Base = declarative_base()

from ..session import session

class Stuff(Base):
    """
    装备、物品等的属性
    """
    __tablename__ = 'stuff_property'

    id = Column(Integer, primary_key=True)
    name = Column(String,comment="物品的中文名字")

    stuff_type = Column(Integer, comment="物品类型，请参考StuffType枚举类型")

    part = Column(Integer, comment="所属位置，0代表不属于某个位置。请参考Part枚举类型")
    is_overlay = Column(Boolean, comment="是否是可叠加的")

    is_bindable = Column(Integer, comment="是否已经绑定")

    decompose_get_stuffs = Column(Integer, comment="分解可以获得的物品列表")

    quality = Column(Integer, comment="参考品质表")  # 枚举类型


    # 新产生的属性将在最小和满属性之间
    minimum_property1 = Column(Integer, comment="属性1")  # 最低属性值，参考skill_achievement_equipment_etc_properties
    minimum_property2 = Column(Integer, comment="属性2")  # 最低属性值，参考skill_achievement_equipment_etc_properties
    minimum_property3 = Column(Integer, comment="属性3")  # 最低属性值，参考skill_achievement_equipment_etc_properties
    minimum_property4 = Column(Integer, comment="属性4")  # 最低属性值，参考skill_achievement_equipment_etc_properties
    minimum_property5 = Column(Integer, comment="属性5")  # 最低属性值，参考skill_achievement_equipment_etc_properties
    minimum_property6 = Column(Integer, comment="属性6")  # 最低属性值，参考skill_achievement_equipment_etc_properties

    complete_property1 = Column(Integer, comment="属性1")  # 满鉴定属性，参考skill_achievement_equipment_etc_properties
    complete_property2 = Column(Integer, comment="属性2")  # 满鉴定属性，参考skill_achievement_equipment_etc_properties
    complete_property3 = Column(Integer, comment="属性3")  # 满鉴定属性，参考skill_achievement_equipment_etc_properties
    complete_property4 = Column(Integer, comment="属性4")  # 满鉴定属性，参考skill_achievement_equipment_etc_properties
    complete_property5 = Column(Integer, comment="属性5")  # 满鉴定属性，参考skill_achievement_equipment_etc_properties
    complete_property6 = Column(Integer, comment="属性6")  # 满鉴定属性，参考skill_achievement_equipment_etc_properties

    introduction = Column(String, comment="说明")

# 增

# 删

# 改

# 查



def get_stuff_by_stuff_id(stuff_id: int):
    """
    根据物品的id查询物品的详细信息

    Parameters:
        stuff_id: int, 物品的id


    Returns:
        stuff_info: Stuff object
            查询到的物品的详细信息

    """
    stuff = session.query(Stuff).filter(Stuff.id == stuff_id).first()
    return stuff

