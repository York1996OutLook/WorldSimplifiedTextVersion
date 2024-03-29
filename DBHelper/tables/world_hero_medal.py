from typing import List

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String,Boolean

from DBHelper.session import session
from Enums import StatusType

from DBHelper.tables.base_table import Entity, Base,Text
from DBHelper.tables.base_table import CustomColumn


class WorldHeroMedal(Entity,Base):
    """
    世界英雄勋章
    """
    __cn__ = "世界英雄勋章"
    __tablename__ = "world_hero_medal"
    id = CustomColumn(Integer, cn="ID", primary_key=True, editable=False,autoincrement=True)

    name = CustomColumn(Text, cn='名称')  # 显式复制并设置 cn 属性

    is_bind = CustomColumn(Boolean, cn="是否绑定",comment="是否绑定")

    @classmethod
    def add_or_update_by_name(cls,
                              *,
                              name: str,
                              is_bind:bool=None,
                              ) -> "WorldHeroMedal":
        record = cls._add_or_update_by_name(kwargs=locals())
        return record

    @classmethod
    def add_or_update_by_id(
            cls,
            *,
            _id: int,
            name: str = None,
            is_bind: bool = None,
    ) -> "WorldHeroMedal":
        record = cls._add_or_update_by_id(kwargs=locals())
        return record
