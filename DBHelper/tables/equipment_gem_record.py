from typing import List

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Float, Boolean

from DBHelper.session import session
from DBHelper.tables.base_table import Basic
from DBHelper.tables.base_table import CustomColumn,Timestamp

Base = declarative_base()


class EquipmentGemRecord(Basic, Base):
    """
    装备镶嵌宝石记录表；一个宝石一个记录表；
    """
    __cn__ = "装备宝石记录表"
    __tablename__ = 'equipment_gem_record'
    id = CustomColumn(Integer, cn="ID", primary_key=True, editable=False,autoincrement=True)
    equipment_id = CustomColumn(Integer, cn="装备", comment="装备记录id")  # todo:待定
    gem_id = CustomColumn(Integer, cn="宝石ID", bind_table="Gem", comment="当前宝石的id")
    success = CustomColumn(Boolean, cn="镶嵌成功", comment="是否镶嵌",default=True)
    inlay_timestamp = CustomColumn(Timestamp, cn="镶嵌时间", comment="镶嵌时间")

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

        record = cls._add_or_update_by_id(kwargs=locals())
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
        records = cls.get_all_by_kwargs(equipment_id=equipment_id)
        return records
