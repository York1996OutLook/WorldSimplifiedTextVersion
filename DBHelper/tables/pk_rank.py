from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Float, Boolean
from typing import Optional, List

from DBHelper.tables.base_table import Basic, Base
from DBHelper.tables.base_table import CustomColumn


class PK_Rank(Basic, Base):
    """
    PK排名表。
    pk后两者名次对调，如果pk的时候失败者的名次靠前，则替换名次。新人的pk rank为总人数。需要查看pk rank的时候，才会看到自己的名词。
    """
    __cn__ = "pk排行榜"
    __tablename__ = 'pk_rank'
    id = CustomColumn(Integer, cn="ID", primary_key=True, editable=False,autoincrement=True)

    pk_rank = CustomColumn(Integer, cn="排行", comment="pk排名次")
    character_id = CustomColumn(Integer, cn="玩家", bind_table="Player", comment="")

    @classmethod
    def add_or_update_by_id(cls,
                            *,
                            _id: int = None,
                            pk_rank: int = None,
                            character_id: int = None
                            ):
        """
        更新或创建PK排名记录
        :param _id: 记录ID
        :param pk_rank: PK排名
        :param character_id:
        :return:
        """
        record = cls._add_or_update_by_id(kwargs=locals())
        return record
