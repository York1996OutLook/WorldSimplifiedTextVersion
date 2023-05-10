from typing import List

from sqlalchemy import Integer, String
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session
from DBHelper.tables.base_table import Basic, Base
from DBHelper.tables.base_table import CustomColumn


class EquipmentQualityDustNum(Basic, Base):
    __cn__ = "分解获得粉尘数量"

    __tablename__ = 'equipment_quality_dust_num'

    min_num = CustomColumn(Integer, cn="最小数量", comment="最小获得数量")
    max_num = CustomColumn(Integer, cn="最大数量", comment="最大获得数量")

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
