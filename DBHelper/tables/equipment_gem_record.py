from typing import List

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

from DBHelper.session import session
from DBHelper.tables.base_table import Basic

Base = declarative_base()


class EquipmentGemRecord(Basic, Base):
    """
    装备镶嵌宝石记录表；一个宝石一个记录表；
    """
    __tablename__ = 'equipment_gem_record'

    equipment_id = Column(Integer, comment="装备id")
    gem_id = Column(Integer, comment="当前宝石的id")
    inlay_time = Column(Integer, comment="镶嵌时间")

    # 增改
    @classmethod
    def add_or_update_by_id(
            cls,
            *,
            _id: int,

            equipment_id: int = None,
            gem_id: int = None
    ) -> "EquipmentGemRecord":
        """
        实际上equipment_id，gem_id不可为空
        """

        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
        return record

    # 查询
    @classmethod
    def get_all_gems_by_equipment_id(cls,
                                     *,
                                     equipment_id: int
                                     ) -> List["EquipmentGemRecord"]:
        """根据装备id查询所有宝石记录

        Args:
        equipment_id (int): 装备id

        Returns:
        List[EquipmentGemRecord]: 宝石记录列表
        """
        records = cls.get_all_by(equipment_id=equipment_id)
        return records
