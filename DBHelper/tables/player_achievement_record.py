from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from typing import List

from DBHelper.tables.base_table import Basic,Base


class PlayerAchievementRecord(Basic,Base):
    """
    将玩家获得的成就记录下来
    """
    __tablename__ = "player_achievement_record"

    character_id = Column(Integer, comment="成就达成人物ID")

    achievement_id = Column(Integer, comment="成就ID")
    achieve_timestamp = Column(Integer, comment="成就达成时间")

    @classmethod
    def add_or_update_by_id(cls, *,
                            _id: int,
                            character_id: int = None,
                            achievement_id: int = None,
                            achieve_timestamp: int = None
                            ):
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
        return record

    @classmethod
    def get_all_by_character_id(cls,*, character_id: int) -> List["PlayerAchievementRecord"]:
        """
        通过玩家ID获取其所有成就记录
        :param character_id: 玩家ID
        :return: List[AchievementRecord]
        """
        records = cls.get_all_by(character_id=character_id)
        return records
