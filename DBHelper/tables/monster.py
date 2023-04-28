from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

Base = declarative_base()

from DBHelper.session import session
from DBHelper.tables.base_table import Entity


# 怪物
class Monster(Entity):
    """
    怪物
    """
    __tablename__ = 'monster'

    exp_value = Column(Integer, comment='被击败后掉落的经验值')
    introduction = Column(String, comment='怪物说明或者背景')

    @classmethod
    def add_or_update_by_name(cls,
                              *,
                              name: str,
                              exp_value: int = None,
                              introduction: str = None
                              ) -> "Monster":

        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_name)
        record = cls._add_or_update_by_name(**fields)
        return record

    @classmethod
    def add_or_update_by_id(
            cls,
            *,
            _id: int,

            name: str = None,
            exp_value: int = None,
            introduction: str = None
            ) -> "Monster":

        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
        return record

# 增

