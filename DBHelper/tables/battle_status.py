from typing import List

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String,Text

from DBHelper.session import session
from DBHelper.tables.base_table import CustomColumn
from Enums import StatusType

from DBHelper.tables.base_table import Entity,Base


class BattleStatus(Entity,Base):
    """
    战斗中的属性,比如中毒,火烧等等;
    """
    __cn__='战斗属性'
    __tablename__ = "battle_status"
    name = CustomColumn(String, cn='名称')  # 显式复制并设置 cn 属性

    status_type = CustomColumn(Integer, cn='状态类型',comment="状态类型")
    effect_expression = CustomColumn(Text, cn='效果说明',comment="效果介绍")

    @classmethod
    def add_or_update_by_name(cls,
                              *,
                              name: str,
                              status_type: int = None,
                              effect_expression: str = None
                              ) -> "BattleStatus":

        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_name)
        record = cls._add_or_update_by_name(**fields)
        return record

    @classmethod
    def add_or_update_by_id(
            cls,
            *,
            _id: int,

            name: str = None,
            status_type: int = None,
            effect_expression: str = None
            ) -> "BattleStatus":

        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
        return record
