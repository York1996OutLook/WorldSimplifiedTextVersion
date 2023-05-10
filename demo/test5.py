from sqlalchemy import Integer, String, Text, Boolean, Float, Column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CustomColumn(Column):
    def unique_params(self, *optionaldict, **kwargs):
        pass

    def params(self, *optionaldict, **kwargs):
        pass

    def __init__(self,
                 *args,
                 bind_type=None,
                 cn: str = None,
                 editable: bool = True,
                 **kwargs):
        super(CustomColumn, self).__init__(*args, **kwargs)
        self.bind_type = bind_type
        self.cn = cn
        self.editable = editable


class Entity:
    # name = CustomColumn(String, cn=1)
    name =1

    def __init__(self):
        super(Entity, self).__init__()
        Entity.name = CustomColumn(String, cn='名称')


class BattleStatus(Entity, Base):
    """
    战斗中的属性,比如中毒,火烧等等;
    """

    __cn__ = '战斗属性'
    __tablename__ = "battle_status"
    _id = CustomColumn(Integer, primary_key=True)


print(BattleStatus.name)
