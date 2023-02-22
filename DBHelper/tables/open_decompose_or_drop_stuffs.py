from typing import List

from sqlalchemy import and_
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session
from Enums import StuffType

Base = declarative_base()


class OpenDecomposeOrDropStuffsRecord(Base):
    """
    打开 分解 掉落的物品记录
    """
    __tablename__ = 'open_decompose_or_drop_stuffs_record'
    id = Column(Integer, primary_key=True)

    source_type = Column(Integer, comment="被分解、打开物品的类型")
    source_id = Column(Integer, comment="被分解、打开物品的id")

    get_stuff_type = Column(Integer, comment="物品的类型，参考枚举类型StuffType。")  # 参考枚举类型
    get_stuff_id = Column(Integer, comment="物品的ID")  # 参考物品id
    get_stuff_prob = Column(Integer, comment="出现的概率，独立计算概率。比如50%A物品，50%B物品，最后的结果可能是空，A，B,A+B四种情况！")

    def __init__(self, *,
                 source_type: StuffType,
                 source_id: int,
                 get_stuff_type: StuffType,
                 get_stuff_id: int,
                 get_stuff_prob: int
                 ):
        self.source_type = source_type
        self.source_id = source_id

        self.get_stuff_type = get_stuff_type
        self.get_stuff_id = get_stuff_id
        self.get_stuff_prob = get_stuff_prob


# 增
def add_by(*,
           source_type: StuffType,
           source_id: int,
           get_stuff_type: StuffType,
           get_stuff_id: int,
           get_stuff_prob: int
           ) -> OpenDecomposeOrDropStuffsRecord:
    """

    :param source_type:
    :param source_id:
    :param get_stuff_type:
    :param get_stuff_id:
    :param get_stuff_prob:
    :return:
    """
    record = OpenDecomposeOrDropStuffsRecord(source_type=source_type,
                                             source_id=source_id,
                                             get_stuff_type=get_stuff_type,
                                             get_stuff_id=get_stuff_id,
                                             get_stuff_prob=get_stuff_prob
                                             )
    session.add(record)
    session.commit()
    return record


def add_gem_box(*, box_id: int, gem_id: int, prob: int)->OpenDecomposeOrDropStuffsRecord:
    """
    新增宝石箱子对应的
    :param box_id:
    :param gem_id:
    :param prob:
    :return:
    """
    return add_by(source_type=StuffType.BOX,
                  source_id=box_id,
                  get_stuff_type=StuffType.GEM,
                  get_stuff_id=gem_id,
                  get_stuff_prob=prob)

def add_monster_drop_equipment(*,mo):

# 删
def delete_box_records_by_box_id(*,
                             box_id: int
                             ):
    """
    删除某个源物品的所有记录，方便后续插入新的记录；
    :param box_id:
    :return:
    """
    session.query(OpenDecomposeOrDropStuffsRecord).filter(
        and_(OpenDecomposeOrDropStuffsRecord.source_type == StuffType.BOX,
             OpenDecomposeOrDropStuffsRecord.source_id == box_id)).delete()
    session.commit()
def delete_records_by_source(*,
                             source_type: StuffType,
                             source_id: int
                             ):
    """
    删除某个源物品的所有记录，方便后续插入新的记录；
    :param source_type:
    :param source_id:
    :return:
    """
    session.query(OpenDecomposeOrDropStuffsRecord).filter(
        and_(OpenDecomposeOrDropStuffsRecord.source_type == source_type,
             OpenDecomposeOrDropStuffsRecord.source_id == source_id)).delete()
    session.commit()
# 改

# 查
