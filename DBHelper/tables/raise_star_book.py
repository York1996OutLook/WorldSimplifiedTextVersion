from typing import List

from sqlalchemy import Integer, String, Boolean,Text
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session
from DBHelper.tables.base_table import Entity
from DBHelper.tables.base_table import CustomColumn

Base = declarative_base()

class RaiseStarBook(Entity,Base):
    __cn__ = "装备强化卷轴"
    __tablename__ = 'raise_star_book'
    id = CustomColumn(Integer, cn="ID", primary_key=True, editable=False,autoincrement=True)

    introduce = CustomColumn(Text, cn="介绍",comment="介绍")

    is_bind = CustomColumn(Boolean, cn="是否绑定",comment="新出现的时候是否已经绑定")

    @classmethod
    def add_or_update_by_name(cls,
                              *,
                              name: str,
                              introduce: str = None,
                              is_bind: bool = None
                              ) -> "RaiseStarBook":

        record = cls._add_or_update_by_name(kwargs=locals())
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

        record = cls._add_or_update_by_id(kwargs=locals())
        return record


# 增

# 删

# 改

# 查

