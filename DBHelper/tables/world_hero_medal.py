from typing import List

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,Boolean

from DBHelper.session import session
from Enums import StatusType

from DBHelper.tables.base_table import Entity, Base


class WorldHeroMedal(Entity,Base):
    """
    世界英雄勋章
    """
    __tablename__ = "world_hero_medal"

    is_bind = Column(Boolean, comment="是否绑定")

    @classmethod
    def add_or_update_by_name(cls,
                              *,
                              name: str,
                              is_bind:bool=None,
                              ) -> "WorldHeroMedal":
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_name)
        record = cls._add_or_update_by_name(**fields)
        return record

    @classmethod
    def add_or_update_by_id(
            cls,
            *,
            _id: int,
            name: str = None,
            is_bind: bool = None,
    ) -> "WorldHeroMedal":
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
        return record
