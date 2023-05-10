import time
from typing import List

from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declarative_base
from DBHelper.tables.base_table import CustomColumn,Timestamp

from DBHelper.session import session
from DBHelper.tables.base_table import Basic,Base


class PlayerPotionRecord(Basic,Base):
    """
    将玩家使用的药品记录下来。每个用户仅有一个使用药剂记录,使用新的药剂会替换原有药剂;
    """
    __cn__ = "玩家药剂使用"
    __tablename__ = "player_potion_record"

    character_id = CustomColumn(Integer, cn="人物ID",comment="药剂使用者的人物ID")
    potion_id = CustomColumn(Integer, cn="药剂ID",comment="药剂类ID")

    take_timestamp = CustomColumn(Timestamp, cn="使用时间",comment="药剂类最新的使用时间")

    @classmethod
    def add_or_update_by_id(cls,
                            *,
                            _id: int = None,
                            character_id: int = None,
                            potion_id: int = None,
                            take_timestamp: int = None
                            ):
        """
        更新或创建药品使用记录
        :param _id: 记录ID
        :param character_id: 药剂使用者的人物ID
        :param potion_id: 药剂类ID
        :param take_timestamp: 药剂类最新的使用时间
        :return: Record
        """
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
        return record

# 删

# 改


# 查


def get_by_character_id(*, character_id: int) -> PlayerPotionRecord:
    """
    根据记录id获取player_potion
    """
    record = session.query(PlayerPotionRecord).filter(PlayerPotionRecord.character_id == character_id).first()
    return record


# other
