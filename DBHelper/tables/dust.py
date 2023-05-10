from typing import List

from sqlalchemy import Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session
from DBHelper.tables.base_table import Basic, Base
from DBHelper.tables.base_table import CustomColumn
from Enums import PartType


class Dust(Basic, Base):
    """
    粉尘
    """
    __cn__ = "粉尘"

    __tablename__ = 'dust'
    name = CustomColumn(String, cn='名称')  # 显式复制并设置 cn 属性

    equipment_part = CustomColumn(Integer, cn='物品部位', bind_type=PartType, comment="对应的装备部位,参考部位类型")
    is_bind = CustomColumn(Boolean, cn='是否绑定', comment="是否为绑定")
    introduce = CustomColumn(String, cn="介绍", comment="介绍")

    @classmethod
    def add_or_update_by_id(cls,
                            *,
                            _id: int = None,
                            name: str = None,
                            equipment_part: int = None,
                            is_bind: bool = None
                            ):
        """
        更新或创建粉尘记录
        :param _id: 记录ID
        :param name: 名称
        :param equipment_part: 对应装备部位
        :param is_bind: 是否绑定
        :return:
        """
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
        return record
