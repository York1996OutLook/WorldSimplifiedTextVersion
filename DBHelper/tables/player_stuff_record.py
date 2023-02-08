from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from typing import List

Base = declarative_base()

from ..session import session


class PlayerStuffRecord(Base):
    """
    装备、物品、称号等的属性
    """
    __tablename__ = 'player_stuff_record'
    id = Column(Integer, primary_key=True)

    character_id = Column(Integer, comment="人物id")
    stuff_id = Column(Integer, comment="物品id")

    stuff_num = Column(Integer, comment="数量")
    is_bind = Column(Boolean, comment="是否已经绑定")
    is_wearing = Column(Boolean, comment="是否穿戴中")

    base_property1 = Column(Integer, comment="属性1")  # 当前属性；参考skill_achievement_equipment_etc_properties
    base_property2 = Column(Integer, comment="属性2")  # 当前属性；参考skill_achievement_equipment_etc_properties
    base_property3 = Column(Integer, comment="属性3")  # 当前属性；参考skill_achievement_equipment_etc_properties
    base_property4 = Column(Integer, comment="属性4")  # 当前属性；参考skill_achievement_equipment_etc_properties
    base_property5 = Column(Integer, comment="属性5")  # 当前属性；参考skill_achievement_equipment_etc_properties
    base_property6 = Column(Integer, comment="属性6")  # 当前属性；参考skill_achievement_equipment_etc_properties

    # 新鉴定出的属性
    temp_property1 = Column(Integer, comment="新鉴定出来的属性1")  # 当前属性；参考skill_achievement_equipment_etc_properties
    temp_property2 = Column(Integer, comment="新鉴定出来的属性2")  # 当前属性；参考skill_achievement_equipment_etc_properties
    temp_property3 = Column(Integer, comment="新鉴定出来的属性3")  # 当前属性；参考skill_achievement_equipment_etc_properties
    temp_property4 = Column(Integer, comment="新鉴定出来的属性4")  # 当前属性；参考skill_achievement_equipment_etc_properties
    temp_property5 = Column(Integer, comment="新鉴定出来的属性5")  # 当前属性；参考skill_achievement_equipment_etc_properties
    temp_property6 = Column(Integer, comment="新鉴定出来的属性6")  # 当前属性；参考skill_achievement_equipment_etc_properties

    # 根据（升星后的数量*加成百分比+1）* 基础属性计算升星后的属性值；
    current_stars_num = Column(Integer, comment="当前升星数量")


# 增

# 删

# 改

# 查
def get_all_wearing_stuffs_by_character_id(character_id: int) -> List[PlayerStuffRecord]:
    """
    查询人物所有正在穿戴着的物品
    :param character_id: 人物ID
    :return: list, 所有正在穿戴着的物品的信息
    """
    stuffs = session.query(PlayerStuffRecord).filter(
        PlayerStuffRecord.character_id == character_id,
        PlayerStuffRecord.is_wearing == True
    ).all()
    session.close()
    return stuffs
