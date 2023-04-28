from typing import List

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from DBHelper.session import session
from Enums import StatusType

from DBHelper.tables.base_table import Entity, Base


class SkillSlot(Entity, Base):
    """
    人物技能槽
    """
    __tablename__ = "skill_slot"

    @classmethod
    def add_or_update_by_name(cls,
                              *,
                              name: str,
                              **kwargs,
                              ) -> "SkillSlot":
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_name)
        record = cls._add_or_update_by_name(**fields)
        return record

    @classmethod
    def add_or_update_by_id(
            cls,
            *,
            _id: int,
            name: str = None,
    ) -> "SkillSlot":
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
        return record
