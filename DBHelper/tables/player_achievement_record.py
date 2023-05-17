from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declarative_base
from typing import List

from DBHelper.tables.base_table import Basic, Base
from DBHelper.tables.base_table import CustomColumn, Timestamp


class PlayerAchievementRecord(Basic, Base):
    """
    将玩家获得的成就记录下来
    """
    __cn__ = "玩家成就记录表"
    __tablename__ = "player_achievement_record"
    id = CustomColumn(Integer, cn="ID", primary_key=True, editable=False,autoincrement=True)

    character_id = CustomColumn(Integer, cn="玩家",bind_table="Player",comment="成就达成人物ID")

    achievement_id = CustomColumn(Integer, cn="成就",bind_table="Achievement",comment="成就ID")
    achieve_timestamp = CustomColumn(Timestamp, cn="达成时间",comment="成就达成时间")

    @classmethod
    def add_or_update_by_id(cls, *,
                            _id: int,
                            character_id: int = None,
                            achievement_id: int = None,
                            achieve_timestamp: int = None
                            ):
        record = cls._add_or_update_by_id(kwargs=locals())
        return record

    @classmethod
    def get_all_by_character_id(cls, *, character_id: int) -> List["PlayerAchievementRecord"]:
        """
        通过玩家ID获取其所有成就记录
        :param character_id: 玩家ID
        :return: List[AchievementRecord]
        """
        records = cls.get_all_by(character_id=character_id)
        return records
