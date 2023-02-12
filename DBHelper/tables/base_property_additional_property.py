from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from DBHelper.session import session

Base = declarative_base()


class BasePropertyAdditionalProperty(Base):
    """
    基础属性会带来的附加属性提升
    """
    __tablename__ = "base_property_additional_property"

    id = Column(Integer, primary_key=True, comment="ID")

    base_property_type = Column(String, comment="参考枚举 BasePropertyType：体质 力量 敏捷 智力 感知")

    attack_increase = Column(Integer, comment="攻击力增加")
    health_increase = Column(Integer, comment="生命值增加")
    mana_increase = Column(Integer, comment="法力值增加")
    attack_attack_speed_increase = Column(Integer, comment="出手速度增加")


# 增
def add_base_property_additional_property(*, base_property_name: int,
                                          attack_increase: int,
                                          health_increase: int,
                                          mana_increase: int,
                                          attack_attack_speed_increase: int
                                          ) -> BasePropertyAdditionalProperty:
    """
    新增一个基础属性表
    :param base_property_name:
    :param attack_increase:
    :param health_increase:
    :param mana_increase:
    :param attack_attack_speed_increase:
    :return:
    """
    new_property = BasePropertyAdditionalProperty(base_property_name=base_property_name,
                                                  attack_increase=attack_increase,
                                                  health_increase=health_increase,
                                                  mana_increase=mana_increase,
                                                  attack_attack_speed_increase=attack_attack_speed_increase)
    session.add(new_property)
    session.commit()

    return new_property


# 删
def delete_property_add_record_by_id(*, record_id: int):
    """
    通过附加属性提升记录ID删除记录
    :param record_id: 附加属性提升记录ID
    :return: None
    """
    session.query(BasePropertyAdditionalProperty).filter(BasePropertyAdditionalProperty.id == record_id).delete()
    session.commit()


# 改
def update_base_property_add_record(*, record_id: int, base_property_name: str = None,
                                    attack_increase: int = None, health_increase: int = None, mana_increase: int = None,
                                    attack_speed_increase: int = None):
    """
    Update a BasePropertyAddRecord object with optional parameters

    :param record_id: ID of the BasePropertyAddRecord object to be updated
    :param base_property_name: (Optional) Name of the base property
    :param attack_increase: (Optional) Increase in attack power
    :param health_increase: (Optional) Increase in hit points
    :param mana_increase: (Optional) Increase in magic points
    :param attack_speed_increase: (Optional) Increase in speed
    :return: Updated BasePropertyAddRecord object, None if no record found
    """

    record = BasePropertyAdditionalProperty.query.filter_by(id=record_id).first()

    if base_property_name is not None:
        record.base_property_name = base_property_name
    if attack_increase is not None:
        record.attack_increase = attack_increase
    if health_increase is not None:
        record.health_increase = health_increase
    if mana_increase is not None:
        record.mana_increase = mana_increase
    if attack_speed_increase is not None:
        record.attack_speed_increase = attack_speed_increase

    session.commit()
    return record

# 查
