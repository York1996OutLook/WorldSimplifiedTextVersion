

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from typing import List

Base = declarative_base()

from DBHelper.session import session


class Stuff(Base):
    """
    装备、物品等的属性
    """
    __tablename__ = 'stuff_property'

    id = Column(Integer, primary_key=True)
    name = Column(String, comment="物品的中文名字")

    stuff_type = Column(Integer, comment="物品类型，请参考StuffType枚举类型")

    part = Column(Integer, comment="所属位置，0代表不属于某个位置。请参考Part枚举类型")
    is_overlay = Column(Boolean, comment="是否是可叠加的")

    is_bindable = Column(Integer, comment="是否已经绑定")

    quality = Column(Integer, comment="参考品质类型")  # 枚举类型

    property1_type = Column(Integer, comment="当前属性1的类型")
    property1_value = Column(Integer, comment="当前属性1的值")

    property2_type = Column(Integer, comment="当前属性2的类型")
    property2_value = Column(Integer, comment="当前属性2的值")

    property3_type = Column(Integer, comment="当前属性3的类型")
    property3_value = Column(Integer, comment="当前属性3的值")

    property4_type = Column(Integer, comment="当前属性4的类型")
    property4_value = Column(Integer, comment="当前属性4的值")


    temp_identify_property1_type = Column(Integer, comment="临时鉴定属性1的类型")
    temp_identify_property1_value = Column(Integer, comment="临时鉴定属性1的值")

    temp_identify_property2_type = Column(Integer, comment="临时鉴定当前属性2的类型")
    temp_identify_property2_value = Column(Integer, comment="临时鉴定当前属性2的值")

    temp_identify_property3_type = Column(Integer, comment="临时鉴定当前属性3的类型")
    temp_identify_property3_value = Column(Integer, comment="临时鉴定当前属性3的值")

    temp_identify_property4_type = Column(Integer, comment="临时鉴定当前属性4的类型")
    temp_identify_property4_value = Column(Integer, comment="临时鉴定当前属性4的值")

    # 新产生的属性将在最小和满属性之间
    introduction = Column(String, comment="说明")
# 增

# 删

# 改

# 查
def get_stuff_by_stuff_id(*,stuff_id: int):
    """
    根据物品的id查询物品的详细信息

    Parameters:
        stuff_id: int, 物品的id


    Returns:
        stuff_info: Stuff object
            查询到的物品的详细信息

    """
    stuff = session.query(Stuff).filter(Stuff.id == stuff_id).first()
    return stuff
