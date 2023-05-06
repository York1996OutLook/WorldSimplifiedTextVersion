import os.path as osp

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

from DBHelper.session import session
from DBHelper.tables.base_table import Entity

from Enums import AdditionalPropertyType
import local_setting
from Utils import tools

Base = declarative_base()


class Gem(Entity,Base):
    __tablename__ = 'gem'

    additional_property_type = Column(Integer, comment="参考AdditionalPropertyType")
    increase = Column(Integer, comment="+1还是+2,3,4,5等")
    is_bind = Column(Boolean, comment="刚出来的时候是否已经绑定")

    @classmethod
    def add_or_update_by_name(cls,
                              *,
                              name: str,
                              additional_property_type: int = None,
                              increase: int = None,
                              is_bind: bool = None
                              ) -> "Gem":
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_name)
        record = cls._add_or_update_by_name(**fields)
        return record

    @classmethod
    def add_or_update_by_id(
            cls,
            *,
            _id: int,

            name: str = None,
            additional_property_type: int = None,
            increase: int = None,
            is_bind: bool = None
    ) -> "Gem":
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
        return record


