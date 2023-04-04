from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from typing import List

from DBHelper.session import session
from Enums import PartType, EquipmentQuality

Base = declarative_base()


class Equipment(Base):
    """
    装备的属性
    """
    __tablename__ = 'equipment'

    id = Column(Integer, primary_key=True)
    name = Column(String, comment="物品的中文名字")

    part = Column(Integer, comment="所属位置，请参考Part枚举类型")

    quality = Column(Integer, comment="参考品质类型 EquipmentQuality")  # 枚举类型

    can_be_identified = Column(Boolean, comment="是否可以被鉴定")

    introduction = Column(String, comment="说明")

    is_bind = Column(Boolean, comment="是否已经绑定")

    def __init__(self,
                 *,
                 name: str,
                 part: PartType,
                 quality: EquipmentQuality,
                 can_be_identified: bool,
                 introduction: str,
                 is_bind: bool
                 ):
        self.name = name
        self.part = part
        self.quality = quality
        self.can_be_identified = can_be_identified
        self.introduction = introduction
        self.is_bind = is_bind


# 增
def add_or_update(*,
                  name: str,
                  part: PartType,
                  quality: EquipmentQuality,
                  can_be_identified: bool,
                  introduction: str,
                  is_bind: bool) -> Equipment:
    """
    新增或者更新数据
    :param name:
    :param part:
    :param quality:
    :param can_be_identified:
    :param introduction:
    :param is_bind:
    :return:
    """
    if is_exists_by_name(name):
        equipment = update_by_name(name=name,
                                   part=part,
                                   quality=quality,
                                   can_be_identified=can_be_identified,
                                   introduction=introduction,
                                   is_bind=is_bind)
    else:
        equipment = add(name=name,
                        part=part,
                        quality=quality,
                        can_be_identified=can_be_identified,
                        introduction=introduction,
                        is_bind=is_bind)
    return equipment


def add(*,
        name: str,
        part: PartType,
        quality: EquipmentQuality,
        can_be_identified: bool,
        introduction: str,
        is_bind: bool
        ) -> Equipment:
    new_equipment = Equipment(
        name=name,
        part=part,
        quality=quality,
        can_be_identified=can_be_identified,
        introduction=introduction,
        is_bind=is_bind
    )
    session.add(new_equipment)
    session.commit()
    return new_equipment


# 删

# 改

def update_by_name(
        name: str,
        part: PartType = None,
        quality: EquipmentQuality = None,
        can_be_identified: bool = None,
        introduction: str = None,
        is_bind: bool = None
):
    equipment = session.query(Equipment).filter_by(name=name).first()
    if part is not None:
        equipment.part = part
    if quality is not None:
        equipment.quality = quality
    if can_be_identified is not None:
        equipment.can_be_identified = can_be_identified
    if introduction is not None:
        equipment.introduction = introduction
    if is_bind is not None:
        equipment.is_bind = is_bind

    session.commit()
    session.refresh(equipment)
    return equipment


# 查
def is_exists_by_name(name: str) -> bool:
    """
    根据名称查询是否存在
    :param name:
    :return:
    """
    record = session.query(Equipment).filter(Equipment.name == name).first()
    return record is not None


def get_by_name(name: str) -> Equipment:
    """
    :param name:
    :return:
    """
    equipment = session.query(Equipment).filter(Equipment.name == name).first()
    return equipment


def get_by_id(*, _id: int) -> Equipment:
    """
    根据装备的id查询物品的详细信息

    Parameters:
        _id: int, 物品的id


    Returns:
        stuff_info: Stuff object
            查询到的物品的详细信息

    """
    equipment = session.query(Equipment).filter(Equipment.id == _id).first()
    return equipment


if __name__ == '__main__':
    ...
