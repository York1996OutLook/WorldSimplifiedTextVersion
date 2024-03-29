from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Float, Boolean
from typing import Optional, List

Base = declarative_base()

from DBHelper.session import session
from DBHelper.tables.base_table import Basic
from DBHelper.tables.base_table import CustomColumn

from Enums import StuffType


class PlayerUseStuffRecord(Basic, Base):
    """
    人物使用书记录表
    """
    __cn__ = "玩家物品使用记录表"
    __tablename__ = 'player_use_stuff_record'
    id = CustomColumn(Integer, cn="ID", primary_key=True, editable=False,autoincrement=True)

    character_id = CustomColumn(Integer, cn="玩家", bind_table="Player", comment="character id")

    use_stuff_type = CustomColumn(Integer, cn="物品类型", bind_type=StuffType, comment="参考StuffType")
    use_stuff_num = CustomColumn(Integer, cn="使用数量", comment="使用数量")

    @classmethod
    def add_or_update_by_id(cls,
                            *,
                            _id: int = None,
                            character_id: int = None,

                            use_stuff_type: int = None,
                            use_stuff_num: int = None,
                            ):
        record = cls._add_or_update_by_id(kwargs=locals())
        return record
