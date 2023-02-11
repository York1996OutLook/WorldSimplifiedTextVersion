
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String,Boolean
from sqlalchemy.ext.declarative import declarative_base

from collections import defaultdict
from typing import Optional,DefaultDict


from Enums import AdditionSourceType,AdditionalPropertyType

Base = declarative_base()
from DBHelper.session import session


class MultiProperties(Base):
    """
    多条属性时候的属性表，后期可能会更新

    """
    __tablename__ = 'multi_properties'

    id = Column(Integer, primary_key=True)
    property_id = Column(Integer,comment="属性的ID，可以重复")

    property_index = Column(Integer, comment="属性索引，可以重复，如果重复的话，代表物品可以是多个属性条目随机选择一个")

    property_type = Column(Integer,comment="属性的类型，参考枚举类型AdditionalPropertyType；")
    property_min = Column(Integer, comment="最小数值")
    property_max = Column(Integer, comment="最大数值")

# 增

# 删

# 改

# 查