from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

from typing import List, Optional

Base = declarative_base()

from ..session import session


class BasePropertyAdditionalProperty(Base):
    """
    基础属性会带来的附加属性提升
    """
    __tablename__ = "base_property_additional_property"

    id = Column(Integer, primary_key=True, comment="ID")

    base_property_name = Column(String, comment="参考基础属性表：体质 力量 敏捷 智力 感知")

    power_increase = Column(Integer, comment="攻击力增加")
    hp_increase = Column(Integer, comment="生命值增加")
    mp_increase = Column(Integer, comment="法力值增加")
    speed_increase = Column(Integer, comment="出手速度增加")

# 增
def add_base_property_additional_property(base_property_name: int,
                                          power_increase: int,
                                          hp_increase: int,
                                          mp_increase: int,
                                          speed_increase: int
                                          )->BasePropertyAdditionalProperty:
    """
    新增一个基础属性表
    :param base_property_name:
    :param power_increase:
    :param hp_increase:
    :param mp_increase:
    :param speed_increase:
    :return:
    """
    new_property = BasePropertyAdditionalProperty(base_property_name=base_property_name,
                                                  power_increase=power_increase,
                                                  hp_increase=hp_increase,
                                                  mp_increase=mp_increase,
                                                  speed_increase=speed_increase)
    session.add(new_property)
    session.commit()

    return new_property



# 删
def delete_property_add_record_by_id(record_id: int):
    """
    通过附加属性提升记录ID删除记录
    :param record_id: 附加属性提升记录ID
    :return: None
    """
    session.query(BasePropertyAdditionalProperty).filter(BasePropertyAdditionalProperty.id == record_id).delete()
    session.commit()


# 改
def update_base_property_add_record(record_id: int, character_id: int = None, base_property_name: str = None,
                                    power_increase: int = None, hp_increase: int = None, mp_increase: int = None,
                                    speed_increase: int = None):
    """
    Update a BasePropertyAddRecord object with optional parameters

    :param record_id: ID of the BasePropertyAddRecord object to be updated
    :param character_id: (Optional) ID of the player
    :param base_property_name: (Optional) Name of the base property
    :param power_increase: (Optional) Increase in attack power
    :param hp_increase: (Optional) Increase in hit points
    :param mp_increase: (Optional) Increase in magic points
    :param speed_increase: (Optional) Increase in speed
    :return: Updated BasePropertyAddRecord object, None if no record found
    """
    record = BasePropertyAdditionalProperty.query.filter_by(id=record_id).first()
    if record:
        if base_property_name is not None:
            record.base_property_name = base_property_name
        if power_increase is not None:
            record.power_increase = power_increase
        if hp_increase is not None:
            record.hp_increase = hp_increase
        if mp_increase is not None:
            record.mp_increase = mp_increase
        if speed_increase is not None:
            record.speed_increase = speed_increase

        session.commit()
        return record
    return None

# 查
