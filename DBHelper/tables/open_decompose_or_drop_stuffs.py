from typing import List

from sqlalchemy import and_
from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session
from DBHelper.tables.base_table import Basic, Base
from DBHelper.tables.base_table import CustomColumn
from Enums import StuffType, AdditionSourceType


class OpenDecomposeOrDropStuffsRecord(Basic, Base):
    """
    打开 分解 掉落的物品记录
    """
    __tablename__ = 'open_decompose_or_drop_stuffs_record'

    source_type = CustomColumn(Integer, cn="物品类型", bind_type=StuffType, comment="被分解、打开物品的类型,参考StuffType")
    source_id = CustomColumn(Integer, cn='物品ID', comment="被分解、打开物品的id")

    get_stuff_type = CustomColumn(Integer, cn="获得物品类型", bind_type=StuffType, comment="物品的类型,参考枚举类型StuffType。")
    get_stuff_id = CustomColumn(Integer, cn='获得物品ID', comment="物品的ID")
    get_stuff_prob = CustomColumn(Integer, cn="获得概率",
                                  comment="最小为1/1000。出现的概率,独立计算概率。比如50%A物品,50%B物品,最后的结果可能是空,A,B,A+B四种情况!")

    @classmethod
    def add_or_update_by_id(cls,
                            *,
                            _id: int,
                            source_type: int = None,
                            source_id: int = None,
                            get_stuff_type: int = None,
                            get_stuff_id: int = None,
                            get_stuff_prob: int = None
                            ):
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
        return record


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


def add_gem_box(*,
                box_id: int,
                gem_id: int,
                prob: int
                ) -> OpenDecomposeOrDropStuffsRecord:
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


def add_monster_drop_equipment(*,
                               monster_id: int,
                               drop_stuff_type: StuffType,
                               drop_stuff_id: int,
                               drop_stuff_prob: int
                               ) -> OpenDecomposeOrDropStuffsRecord:
    """

    :param monster_id:boss编号
    :param drop_stuff_type:掉落物品的类型
    :param drop_stuff_id:掉落物品的id
    :param drop_stuff_prob:掉落物品的概率
    :return:
    """
    return add_by(
        source_type=StuffType.MONSTER,
        source_id=monster_id,
        get_stuff_type=drop_stuff_type,
        get_stuff_id=drop_stuff_id,
        get_stuff_prob=drop_stuff_prob,
    )


# 删
def delete_equipment_decompose_get_stuffs(*, equipment_id: int):
    session.query(OpenDecomposeOrDropStuffsRecord).filter(
        and_(OpenDecomposeOrDropStuffsRecord.source_type == StuffType.EQUIPMENT,
             OpenDecomposeOrDropStuffsRecord.source_id == equipment_id)).delete()
    session.commit()


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
def get_by(*,
           source_type: StuffType,
           source_id: int
           ) -> List[OpenDecomposeOrDropStuffsRecord]:
    drops = session.query(OpenDecomposeOrDropStuffsRecord).filter(
        OpenDecomposeOrDropStuffsRecord.source_type == source_type,
        OpenDecomposeOrDropStuffsRecord.source_id == source_id).all()
    return drops


def get_monster_drop_equipments(*,
                                monster_id: int,
                                ) -> List[OpenDecomposeOrDropStuffsRecord]:
    """

    :param monster_id:boss编号
    :return:
    """

    drops = get_by(source_type=StuffType.MONSTER, source_id=monster_id)
    return drops
