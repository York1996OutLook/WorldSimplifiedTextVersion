from typing import List

from sqlalchemy import Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session
from DBHelper.tables.base_table import Entity
from DBHelper.tables.base_table import CustomColumn

Base = declarative_base()

class RaiseStarBook(Entity,Base):
    __cn__ = "装备强化卷轴"
    __tablename__ = 'raise_star_book'

    introduce = CustomColumn(String, cn="介绍",comment="介绍")

    is_bind = CustomColumn(Boolean, cn="是否绑定",comment="新出现的时候是否已经绑定")

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

