from typing import List, Tuple

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session
from DBHelper.tables.base_table import Basic,Base
from Utils.tools import find_smallest_missing
from Enums import StuffType


class EquipmentStarRecord(Basic,Base):
    """
    装备、物品、称号等的属性
    """
    __tablename__ = 'equipment_star_record'

    equipment_record_id=Column(Integer, comment="装备记录id")
    cur_star_num = Column(Integer, comment="当前升星数量，如果没有星星，则不在此表中存储")

    @classmethod
    def add_or_update_by_id(cls,
                            *,
                            _id: int = None,
                            equipment_record_id: int = None,
                            cur_star_num: int = None,
                            ):
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
        return record

# 增

# 删

# 改


