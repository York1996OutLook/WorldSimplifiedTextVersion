from typing import List, Tuple

from sqlalchemy import Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session
from DBHelper.tables.base_table import Basic, Base
from DBHelper.tables.base_table import CustomColumn

from Utils.tools import find_smallest_missing
from Enums import StuffType


class EquipmentStarRecord(Basic, Base):
    """
    装备、物品、称号等的属性
    """
    __cn__ = "装备升星记录表"
    __tablename__ = 'equipment_star_record'
    id = CustomColumn(Integer, cn="ID", primary_key=True, editable=False,autoincrement=True)
    equipment_record_id = CustomColumn(Integer, cn='装备', comment="装备记录id")  # todo
    cur_star_num = CustomColumn(Integer, cn="当前升星数量", comment="当前升星数量，如果没有星星，则不在此表中存储")

    @classmethod
    def add_or_update_by_id(cls,
                            *,
                            _id: int = None,
                            equipment_record_id: int = None,
                            cur_star_num: int = None,
                            ):
        record = cls._add_or_update_by_id(kwargs=locals())
        return record

# 增

# 删

# 改
