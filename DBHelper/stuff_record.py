from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from typing import List

Base = declarative_base()

# 创建数据库连接引擎
engine = create_engine('sqlite:///example.db')

# 创建会话
Session = sessionmaker(bind=engine)
session = Session()


class StuffRecord(Base):
    """
    装备、物品等的属性
    """
    __tablename__ = 'stuff_record'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    part = Column(Integer, comment="所属位置")
    is_bound = Column(Integer, comment="是否已经绑定")
    decompose_get_stuffs = Column(String, comment="分解可以获得的物品列表")

    quality = Column(Integer, comment="参考品质表")  # 枚举类型

    complete_property1 = Column(Integer, comment="属性1")  # 为属性id的列表.满鉴定属性
    complete_property2 = Column(Integer, comment="属性2")  # 为属性id的列表.满鉴定属性
    complete_property3 = Column(Integer, comment="属性3")  # 为属性id的列表.满鉴定属性
    complete_property4 = Column(Integer, comment="属性4")  # 为属性id的列表.满鉴定属性

    property1 = Column(Integer, comment="属性1")  # 为属性id的列表.当前属性；
    property2 = Column(Integer, comment="属性2")  # 为属性id的列表.当前属性；
    property3 = Column(Integer, comment="属性3")  # 为属性id的列表.当前属性；
    property4 = Column(Integer, comment="属性4")  # 为属性id的列表.当前属性；

    introduction = Column(String, comment="说明")
