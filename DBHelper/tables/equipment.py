from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from typing import List

from DBHelper.session import session

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


# 增

# 删

# 改

# 查
def get_equipment_by_equipment_id(*, equipment_id: int) -> Equipment:
    """
    根据装备的id查询物品的详细信息

    Parameters:
        equipment_id: int, 物品的id


    Returns:
        stuff_info: Stuff object
            查询到的物品的详细信息

    """
    equipments = session.query(Equipment).filter(Equipment.id == equipment_id).first()
    return equipments


if __name__ == '__main__':
    ...
