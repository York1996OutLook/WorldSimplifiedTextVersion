import os.path as osp

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Float, Boolean, Text

from DBHelper.session import session
from DBHelper.tables.base_table import CustomColumn
from DBHelper.tables.base_table import Entity

from Enums import AdditionalPropertyType
import local_setting
from Utils import tools

Base = declarative_base()


class Gem(Entity, Base):
    __cn__ = "宝石"

    __tablename__ = 'gem'
    name = CustomColumn(String, cn='名称')  # 显式复制并设置 cn 属性

    additional_property_type = CustomColumn(Integer,
                                            cn="属性",
                                            bind_type=AdditionalPropertyType,
                                            comment="参考AdditionalPropertyType")
    increase = CustomColumn(Integer, cn="增加值", comment="+1还是+2,3,4,5等") # todo:做成枚举类型
    is_bind = CustomColumn(Boolean, cn="是否绑定", comment="刚出来的时候是否已经绑定")
    introduce = CustomColumn(Text, cn="介绍")

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
