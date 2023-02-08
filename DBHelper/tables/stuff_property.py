from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from typing import List

Base = declarative_base()

from ..session import session

class StuffProperty(Base):
    """
    装备、物品等的属性
    """
    __tablename__ = 'stuff_property'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    stuff_type = Column(Integer, comment="物品类型，请参考StuffType枚举类型")

    part = Column(Integer, comment="所属位置，0代表不属于某个位置。请参考Part枚举类型")
    is_overlay = Column(Boolean, comment="是否是可叠加的")

    is_bindable = Column(Integer, comment="是否已经绑定")

    decompose_get_stuffs = Column(Integer, comment="分解可以获得的物品列表")

    quality = Column(Integer, comment="参考品质表")  # 枚举类型

    complete_property1 = Column(Integer, comment="属性1")  # 为属性id的列表.满鉴定属性，参考skill_achievement_equipment_etc_properties
    complete_property2 = Column(Integer, comment="属性2")  # 为属性id的列表.满鉴定属性，参考skill_achievement_equipment_etc_properties
    complete_property3 = Column(Integer, comment="属性3")  # 为属性id的列表.满鉴定属性，参考skill_achievement_equipment_etc_properties
    complete_property4 = Column(Integer, comment="属性4")  # 为属性id的列表.满鉴定属性，参考skill_achievement_equipment_etc_properties
    complete_property5 = Column(Integer, comment="属性5")  # 为属性id的列表.满鉴定属性，参考skill_achievement_equipment_etc_properties
    complete_property6 = Column(Integer, comment="属性6")  # 为属性id的列表.满鉴定属性，参考skill_achievement_equipment_etc_properties

    introduction = Column(String, comment="说明")
