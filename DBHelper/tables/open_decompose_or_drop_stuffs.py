from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from typing import List

Base = declarative_base()
from ..session import session

class OpenDecomposeOrDropStuffs(Base):
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

    stuff1_type = Column(Integer, comment="物品的类型，参考枚举类型StuffType")  # 参考枚举类型
    stuff1_id = Column(Integer, comment="物品的ID")  # 参考物品id
    stuff1_percent = Column(Integer, comment="出现的概率，独立计算概率。比如50%A物品，50%B物品，最后的结果可能是空，A，B,A+B四种情况！")

    stuff2_type = Column(Integer, comment="物品的类型，参考枚举类型StuffType")  # 参考枚举类型
    stuff2_id = Column(Integer, comment="物品的ID")  # 参考物品id
    stuff2_percent = Column(Integer, comment="出现的概率，独立计算概率。比如50%A物品，50%B物品，最后的结果可能是空，A，B,A+B四种情况！")

    stuff3_type = Column(Integer, comment="物品的类型，参考枚举类型StuffType")  # 参考枚举类型
    stuff3_id = Column(Integer, comment="物品的ID")  # 参考物品id
    stuff3_percent = Column(Integer, comment="出现的概率，独立计算概率。比如50%A物品，50%B物品，最后的结果可能是空，A，B,A+B四种情况！")

    stuff4_type = Column(Integer, comment="物品的类型，参考枚举类型StuffType")  # 参考枚举类型
    stuff4_id = Column(Integer, comment="物品的ID")  # 参考物品id
    stuff4_percent = Column(Integer, comment="出现的概率，独立计算概率。比如50%A物品，50%B物品，最后的结果可能是空，A，B,A+B四种情况！")

    stuff5_type = Column(Integer, comment="物品的类型，参考枚举类型StuffType")  # 参考枚举类型
    stuff5_id = Column(Integer, comment="物品的ID")  # 参考物品id
    stuff5_percent = Column(Integer, comment="出现的概率，独立计算概率。比如50%A物品，50%B物品，最后的结果可能是空，A，B,A+B四种情况！")

    stuff6_type = Column(Integer, comment="物品的类型，参考枚举类型StuffType") # 参考枚举类型
    stuff6_id = Column(Integer, comment="物品的ID") # 参考物品id
    stuff6_percent = Column(Integer, comment="出现的概率，独立计算概率。比如50%A物品，50%B物品，最后的结果可能是空，A，B,A+B四种情况！")

    stuff7_type = Column(Integer, comment="物品的类型，参考枚举类型StuffType") # 参考枚举类型
    stuff7_id = Column(Integer, comment="物品的ID") # 参考物品id
    stuff7_percent = Column(Integer, comment="出现的概率，独立计算概率。比如50%A物品，50%B物品，最后的结果可能是空，A，B,A+B四种情况！")

    stuff8_type = Column(Integer, comment="物品的类型，参考枚举类型StuffType") # 参考枚举类型
    stuff8_id = Column(Integer, comment="物品的ID") # 参考物品id
    stuff8_percent = Column(Integer, comment="出现的概率，独立计算概率。比如50%A物品，50%B物品，最后的结果可能是空，A，B,A+B四种情况！")

    stuff9_type = Column(Integer, comment="物品的类型，参考枚举类型StuffType") # 参考枚举类型
    stuff9_id = Column(Integer, comment="物品的ID") # 参考物品id
    stuff9_percent = Column(Integer, comment="出现的概率，独立计算概率。比如50%A物品，50%B物品，最后的结果可能是空，A，B,A+B四种情况！")

    stuff10_type = Column(Integer, comment="物品的类型，参考枚举类型StuffType") # 参考枚举类型
    stuff10_id = Column(Integer, comment="物品的ID") # 参考物品id
    stuff10_percent = Column(Integer, comment="出现的概率，独立计算概率。比如50%A物品，50%B物品，最后的结果可能是空，A，B,A+B四种情况！")

    stuff11_type = Column(Integer, comment="物品的类型，参考枚举类型StuffType") # 参考枚举类型
    stuff11_id = Column(Integer, comment="物品的ID") # 参考物品id
    stuff11_percent = Column(Integer, comment="出现的概率，独立计算概率。比如50%A物品，50%B物品，最后的结果可能是空，A，B,A+B四种情况！")

    stuff12_type = Column(Integer, comment="物品的类型，参考枚举类型StuffType") # 参考枚举类型
    stuff12_id = Column(Integer, comment="物品的ID") # 参考物品id
    stuff12_percent = Column(Integer, comment="出现的概率，独立计算概率。比如50%A物品，50%B物品，最后的结果可能是空，A，B,A+B四种情况！")

    stuff13_type = Column(Integer, comment="物品的类型，参考枚举类型StuffType") # 参考枚举类型
    stuff13_id = Column(Integer, comment="物品的ID") # 参考物品id
    stuff13_percent = Column(Integer, comment="出现的概率，独立计算概率。比如50%A物品，50%B物品，最后的结果可能是空，A，B,A+B四种情况！")

    stuff14_type = Column(Integer, comment="物品的类型，参考枚举类型StuffType") # 参考枚举类型
    stuff14_id = Column(Integer, comment="物品的ID") # 参考物品id
    stuff14_percent = Column(Integer, comment="出现的概率，独立计算概率。比如50%A物品，50%B物品，最后的结果可能是空，A，B,A+B四种情况！")

    stuff15_type = Column(Integer, comment="物品的类型，参考枚举类型StuffType") # 参考枚举类型
    stuff15_id = Column(Integer, comment="物品的ID") # 参考物品id
    stuff15_percent = Column(Integer, comment="出现的概率，独立计算概率。比如50%A物品，50%B物品，最后的结果可能是空，A，B,A+B四种情况！")

    stuff16_type = Column(Integer, comment="物品的类型，参考枚举类型StuffType") # 参考枚举类型
    stuff16_id = Column(Integer, comment="物品的ID") # 参考物品id
    stuff16_percent = Column(Integer, comment="出现的概率，独立计算概率。比如50%A物品，50%B物品，最后的结果可能是空，A，B,A+B四种情况！")

    introduction = Column(String, comment="说明")
