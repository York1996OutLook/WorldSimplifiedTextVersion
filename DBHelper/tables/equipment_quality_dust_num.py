from typing import List

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session
from DBHelper.tables.base_table import Basic,Base


class EquipmentQualityDustNum(Basic,Base):
    """
    升星概率表

    """
    __tablename__ = 'equipment_quality_dust_num'

    min_num = Column(Integer, comment="最小获得数量")
    max_num = Column(Integer, comment="最大获得数量")

    @classmethod
    def add_or_update_by_id(cls,
                            *,
                            _id: int,
                            min_num: int = None,
                            max_num: int = None
                            ):
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
        return record
