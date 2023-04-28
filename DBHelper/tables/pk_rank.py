from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean
from typing import Optional, List

from DBHelper.tables.base_table import Basic,Base


class PK_Rank(Basic,Base):
    """
    PK排名表。
    pk后两者名次对调，如果pk的时候失败者的名次靠前，则替换名次。新人的pk rank为总人数。需要查看pk rank的时候，才会看到自己的名词。
    """
    __tablename__ = 'pk_rank'

    pk_rank = Column(Integer, comment="pk排名次")
    player_id = Column(Integer, comment="QQ")

    @classmethod
    def add_or_update_by_id(cls,
                            *,
                            _id: int = None,
                            pk_rank: int = None,
                            player_id: int = None
                            ):
        """
        更新或创建PK排名记录
        :param _id: 记录ID
        :param pk_rank: PK排名
        :param player_id: QQ
        :return:
        """
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
        return record
