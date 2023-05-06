from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean
from typing import Optional, List

Base = declarative_base()

from DBHelper.session import session
from DBHelper.tables.base_table import Basic


class PlayerUseStuffRecord(Basic, Base):
    """
    人物使用书记录表
    """
    __tablename__ = 'player_use_stuff_record'

    player_id = Column(Integer, comment="QQ")

    use_stuff_type=Column(Integer,comment="参考StuffType")
    current_level = Column(Integer, comment='当前等级')
    current_experience = Column(Integer, comment='当前经验值,为当前经验值')

    game_sign = Column(String, comment="游戏中的签名,可以被其他角色查看到属性")

    gold_num = Column(Integer, comment="黄金数量,游戏唯一游戏币")

    achievement_id = Column(Integer, comment="成就id")

    @classmethod
    def add_or_update_by_id(cls,
                            *,
                            _id: int = None,
                            nickname: str = None,
                            player_id: int = None,
                            first_login_timestamp: int = None,
                            current_level: int = None,
                            current_experience: int = None,
                            game_sign: str = None,
                            gold_num: int = None,
                            achievement_id: int = None
                            ):
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
        return record
