from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

from DBHelper.session import session
from DBHelper.tables.base_table import Basic,Base
from Enums import BattleType

class PlayerBattleRecord(Basic,Base):
    """
    战斗中记录表
    """
    __tablename__ = "player_battle_record"
    battle_type = Column(Integer, comment="战斗类型,参考BattleType")

    positive_character_id = Column(Integer, comment="主动攻击角色ID")
    passive_character_id = Column(Integer, comment="被动攻击角色ID")

    positive_won = Column(Boolean, comment="主动攻击人是否胜利")
    battle_text = Column(String, comment="战斗产生的文字说明")

    @classmethod
    def add_or_update_by_id(cls,
                            *,
                            _id: int,
                            battle_type: int = None,
                            positive_character_id: int = None,
                            passive_character_id: int = None,
                            positive_won: bool = None,
                            battle_text: str = None
                            ):
        """
        更新或创建战斗记录
        :param _id: 记录ID
        :param battle_type: 战斗类型
        :param positive_character_id: 主动攻击角色ID
        :param passive_character_id: 被动攻击角色ID
        :param positive_won: 主动攻击人是否胜利
        :param battle_text: 战斗产生的文字说明
        :return:
        """
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
        return record

    # 改
    @classmethod
    def update_won(cls,*, record_id: int, positive_won: bool) -> "PlayerBattleRecord":

        record=cls.update_kwargs_by_id(_id=record_id,positive_won=positive_won)
        return record

    @classmethod
    def update_text(cls,*, record_id: int, battle_text: str) -> "PlayerBattleRecord":

        record=cls.update_kwargs_by_id(_id=record_id,battle_text=battle_text)
        return record

    @classmethod
    def update_positive_id(cls,*, record_id: int, positive_character_id: int) -> "PlayerBattleRecord":
        record=cls.update_kwargs_by_id(_id=record_id,positive_character_id=positive_character_id)
        return record


# 查询
    @classmethod
    def get_battles_by_positive_id(cls,*, positive_id: int):
        """
        查询主动攻击者是positive_id的所有战斗记录
        """
        records=cls.get_all_by(positive_id=positive_id)
        return records

    @classmethod
    def get_battles_by_passive_id(cls,*, passive_id: int):
        """
        查询被动攻击者是passive_id的所有战斗记录
        """
        records=cls.get_all_by(passive_id=passive_id)
        return records

def get_battles_by_battle_type(*, battle_type: BattleType):
    """
    查询战斗类型为battle_type的所有战斗记录
    """
    return session.query(PlayerBattleRecord).filter_by(battle_type=battle_type).all()


def get_battles_by_result(*, positive_won: bool):
    """
    查询主动攻击者胜利/失败的所有战斗记录
    """
    return session.query(PlayerBattleRecord).filter_by(positive_won=positive_won).all()

