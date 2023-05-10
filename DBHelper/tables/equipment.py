from sqlalchemy import Integer, String, Boolean,Text
from sqlalchemy.ext.declarative import declarative_base
from typing import List

from DBHelper.session import session
from DBHelper.tables.base_table import Entity
from Enums import PartType, EquipmentQuality
from DBHelper.tables.base_table import CustomColumn

Base = declarative_base()


class Equipment(Entity, Base):
    """
    装备的属性
    """
    __cn__ = "装备原型"
    __tablename__ = 'equipment'
    name = CustomColumn(String, cn='名称')  # 显式复制并设置 cn 属性

    part = CustomColumn(Integer, cn="类型/部位",bind_type=PartType, comment="所属位置,请参考Part枚举类型")

    quality = CustomColumn(Integer, cn="品质",bind_type=EquipmentQuality, comment="参考品质类型 EquipmentQuality")

    can_be_identified = CustomColumn(Boolean, cn="可被鉴定", comment="是否可以被鉴定")

    introduction = CustomColumn(Text, cn="介绍", comment="说明")

    is_bind = CustomColumn(Boolean, cn="是否被绑定", comment="是否已经绑定")

    @classmethod
    def add_or_update_by_name(cls,
                              *,
                              name: str,

                              part: int = None,
                              quality: int = None,

                              can_be_identified: bool = None,

                              introduction: str = None,
                              is_bind: bool = None
                              ) -> "Equipment":
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_name)
        record = cls._add_or_update_by_name(**fields)
        return record

    # 改
    @classmethod
    def add_or_update_by_id(
            cls,
            *,
            _id: int,

            name: str = None,
            part: int = None,
            quality: int = None,

            can_be_identified: bool = None,

            introduction: str = None,
            is_bind: bool = None
    ) -> "Equipment":
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
        return record
