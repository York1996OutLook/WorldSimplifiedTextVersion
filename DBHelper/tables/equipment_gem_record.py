from typing import List

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

from DBHelper.session import session

Base = declarative_base()


class EquipmentGemRecord(Base):
    __tablename__ = 'equipment_gem_record'

    id = Column(Integer, primary_key=True)

    equipment_id = Column(Integer, comment="装备id")
    gem_id = Column(Integer, comment="当前宝石的id")


# 查询
def get_all_gems_by_equipment_id(*,
                                 equipment_id: int
                                 ) -> List[EquipmentGemRecord]:
    """根据装备id查询所有宝石记录

    Args:
    equipment_id (int): 装备id

    Returns:
    List[EquipmentGemRecord]: 宝石记录列表
    """

    gems = session.query(EquipmentGemRecord).filter(EquipmentGemRecord.equipment_id == equipment_id).all()
    return gems
