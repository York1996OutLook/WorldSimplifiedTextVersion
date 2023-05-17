from typing import List, Tuple

from sqlalchemy import Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session
from DBHelper.tables.base_table import Basic, Base
from DBHelper.tables.base_table import CustomColumn
from Utils.tools import find_smallest_missing
from Enums import StuffType, GemInlayingStatus


class PlayerStuffRecord(Basic, Base):
    """
    装备、物品、称号等的属性
    """
    __cn__ = "玩家物品记录表"
    __tablename__ = 'player_stuff_record'
    id = CustomColumn(Integer, cn="ID", primary_key=True, editable=False,autoincrement=True)

    character_id = CustomColumn(Integer,cn="玩家", comment="人物id")
    stuff_type = CustomColumn(Integer,cn="物品类型", bind_type=StuffType, comment="物品的类型,参考StuffType")
    stuff_id = CustomColumn(Integer, cn="物品",comment="物品id")    # todo

    stuff_num = CustomColumn(Integer,cn="数量", comment="数量")
    is_bind = CustomColumn(Boolean,cn="是否绑定", comment="是否已经绑定")
    is_wearing = CustomColumn(Boolean,cn="是否穿戴中", comment="是否穿戴中")

    position_in_bag = CustomColumn(Integer,cn="在背包中的位置", comment="在背包中的位置,从1开始,目前没有设定背包大小.0代表没有在背包中。")

    # current_stars_num = CustomColumn(Integer,cn="当前升星数量", comment="当前升星数量")   # 可以通过装备升星表获得
    # gem_inlaying_status = CustomColumn(Integer,cn="玩家", bind_type=GemInlayingStatus, comment="宝石镶嵌的状态。参考 GemInlayingStatus")  # 可以通过装备宝石表获得

    @classmethod
    def add_or_update_by_id(cls,
                            *,
                            _id: int = None,
                            character_id: int = None,
                            stuff_type: int = None,
                            stuff_id: int = None,
                            stuff_num: int = None,
                            is_bind: bool = None,
                            is_wearing: bool = None,
                            position_in_bag: int = None,
                            current_stars_num: int = None,
                            gem_inlaying_status: int = None
                            ):
        record = cls._add_or_update_by_id(kwargs=locals())
        return record


# 增

# 删

# 改
def update_bag_stuffs_position(*,
                               stuff_position_list: List[Tuple[PlayerStuffRecord, int]]
                               ):
    """

    :param stuff_position_list:
    :return:
    """
    for stuff, new_position in stuff_position_list:
        stuff.position_in_bag = new_position
    session.commit()


def update_stuff_wearing_and_position(*,
                                      stuff_record_id: int,
                                      is_wearing: bool = None,
                                      new_position: int = None
                                      ) -> PlayerStuffRecord:
    """
    更新物品穿戴情况和位置信息
    该函数将一件物品的穿戴情况和位置信息更新为新的穿戴情况和位置信息

    Parameters
    ----------
    stuff_record_id : int
        物品id
    is_wearing : bool
        是否穿戴中
    new_position : int
        分配的位置信息
    Returns
    -------
    dict
        返回更新后的物品信息
    """
    record = session.query(PlayerStuffRecord).filter_by(id=stuff_record_id).first()
    if is_wearing:
        record.is_wearing = is_wearing
    if new_position:
        record.position_in_bag = new_position
    session.commit()
    return record


# 查


def get_all_wearing_equipments_by_character_id(*,
                                               character_id: int
                                               ) -> List[PlayerStuffRecord]:
    """
    查询人物所有正在穿戴着的物品
    :param character_id: 人物ID
    :return: list, 所有正在穿戴着的物品的信息
    """
    stuffs = session.query(PlayerStuffRecord).filter(
        PlayerStuffRecord.character_id == character_id,
        PlayerStuffRecord.is_wearing == True
    ).all()
    return stuffs


def get_all_in_bag_stuffs_by_character_id(*,
                                          character_id: int
                                          ) -> List[PlayerStuffRecord]:
    """
    查询人物所有正在穿戴着的物品。没有穿着，意味着是在背包中；
    :param character_id: 人物ID
    :return: list, 所有正在穿戴着的物品的信息
    """
    stuffs = session.query(PlayerStuffRecord).filter(
        PlayerStuffRecord.character_id == character_id,
        PlayerStuffRecord.is_wearing == False  # 没有穿着，意味着是在背包中；
    ).all()
    return stuffs


# other

# 获取当面背包没有被占用的最小位置
def get_min_unused_bag_position(*,
                                character_id: int
                                ) -> int:
    """
    获取某个角色最小的未用的背包位置。
    """
    bag_stuffs = get_all_in_bag_stuffs_by_character_id(character_id=character_id)

    positions = []
    for stuff in bag_stuffs:
        positions.append(stuff.position_in_bag)

    available_position = find_smallest_missing(positions=positions)
    return available_position


# 往背包中的某个位置插入物品，并且这个物品之前之前没有穿戴着；
def insert_stuff_to_player_bag(*,
                               stuff_record_id: int,
                               character_id: int
                               ) -> PlayerStuffRecord:
    """
    往用户背包中插入新的物品
    :param stuff_record_id:
    :param character_id:
    :return:
    """
    available_position = get_min_unused_bag_position(
        character_id=character_id,
    )
    player_stuff_record = get_by_record_id(record_id=stuff_record_id)

    record = add(
        character_id=character_id,
        stuff_id=player_stuff_record.stuff_id,
        stuff_type=player_stuff_record.stuff_type,
        stuff_num=player_stuff_record.stuff_num,
        is_bind=player_stuff_record.is_bind,
        is_wearing=False,
        position_in_bag=available_position,

        current_stars_num=player_stuff_record.current_stars_num,
    )
    session.add(record)
    session.commit()
    return record


def wearing_stuff_to_bag(*,
                         character_id: int,
                         player_stuff_record_id: int
                         ) -> PlayerStuffRecord:
    """
    玩家穿着的物品放到背包中；
    :param character_id:
    :param player_stuff_record_id:
    :return:
    """
    available_position = get_min_unused_bag_position(
        character_id=character_id,
    )
    record = update_stuff_wearing_and_position(stuff_record_id=player_stuff_record_id,
                                               is_wearing=False,
                                               new_position=available_position)
    session.commit()
    session.refresh(record)
    return record


def bag_stuff_to_wearing(*,
                         player_stuff_record_id: int
                         ) -> PlayerStuffRecord:
    """

    :param player_stuff_record_id:
    :return:
    """
    record = update_stuff_wearing_and_position(stuff_record_id=player_stuff_record_id,
                                               is_wearing=False)
    session.commit()
    session.refresh(record)
    return record
