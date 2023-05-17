from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Float, Boolean,Text

Base = declarative_base()

from DBHelper.session import session
from DBHelper.tables.base_table import Entity
from DBHelper.tables.base_table import CustomColumn


# 怪物
class Monster(Entity, Base):
    """
    怪物
    """
    __cn__ = "怪物"

    __tablename__ = 'monster'
    id = CustomColumn(Integer, cn="ID", primary_key=True, editable=False,autoincrement=True)

    name = CustomColumn(Text,cn="名称",comment='')

    exp_value = CustomColumn(Integer, cn='经验值', comment='被击败后掉落的经验值')
    introduce = CustomColumn(Text, cn="介绍")
    deposit = CustomColumn(Integer, cn="押金", default=0, comment='押金')

    @classmethod
    def add_or_update_by_name(cls,
                              *,
                              name: str,
                              exp_value: int = None,
                              introduction: str = None,
                              deposit: int = None
                              ) -> "Monster":
        record = cls._add_or_update_by_name(kwargs=locals())
        return record

    @classmethod
    def add_or_update_by_id(
            cls,
            *,
            _id: int,

            name: str = None,
            exp_value: int = None,
            introduction: str = None,
            deposit: int = None
    ) -> "Monster":
        record = cls._add_or_update_by_id(kwargs=locals())
        return record

# 增
