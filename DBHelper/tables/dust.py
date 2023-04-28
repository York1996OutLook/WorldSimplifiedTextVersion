from typing import List

from sqlalchemy import Column, Integer, String,Boolean
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session
from DBHelper.tables.base_table import Basic,Base


class Dust(Basic,Base):
    """
    粉尘
    """
    __tablename__ = 'dust'

    equipment_part = Column(Integer, comment="对应的装备部位,参考部位类型")
    is_bind = Column(Boolean, comment="是否为绑定")

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

