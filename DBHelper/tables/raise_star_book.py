from typing import List

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session
from DBHelper.tables.base_table import Entity

Base = declarative_base()

class RaiseStarBook(Entity):
    """
    打开 分解 掉落的物品记录
    """
    __tablename__ = 'identify_book'
    introduce = Column(String, comment="介绍")

    is_bind = Column(Boolean, comment="新出现的时候是否已经绑定")

    @classmethod
    def add_or_update_by_name(cls,
                              *,
                              name: str,
                              introduce: str = None,
                              is_bind: bool = None
                              ) -> "RaiseStarBook":

        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_name)
        record = cls._add_or_update_by_name(**fields)
        return record

    @classmethod
    def add_or_update_by_id(
            cls,
            *,
            _id: int,

            name: str = None,
            introduce: str = None,
            is_bind: bool = None
            ) -> "RaiseStarBook":

        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
        return record


# 增

# 删

# 改

# 查

