from typing import List

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session
from Utils.tools import find_smallest_missing

Base = declarative_base()


class PlayerStuffRecord(Base):
    """
    装备、物品、称号等的属性
    """
    __tablename__ = 'player_stuff_record'
    id = Column(Integer, primary_key=True)

    character_id = Column(Integer, comment="人物id")
    stuff_id = Column(Integer, comment="物品id")

    stuff_num = Column(Integer, comment="数量")
    is_bind = Column(Boolean, comment="是否已经绑定")
    is_wearing = Column(Boolean, comment="是否穿戴中")  # 如果没有穿戴中，则认为是在背包中；

    position_in_bag = Column(Integer, comment="在背包中的位置，从1开始，目前没有设定背包大小.0代表没有在背包中。")

    # 根据（升星后的数量*加成百分比+1）* 基础属性计算升星后的属性值；
    current_stars_num = Column(Integer, comment="当前升星数量")
    gem_inlaying_status = Column(Integer, comment="宝石镶嵌的状态。参考 GemInlayingStatus")


# 增
def add_player_stuff_record(*,
                            character_id: int,
                            stuff_id: int,
                            stuff_num: int,
                            is_bind: bool,
                            is_wearing: bool,
                            position_in_bag: int,

                            current_stars_num: int) -> PlayerStuffRecord:
    """
    新增一条玩家物品记录
    :param character_id: 人物id
    :param stuff_id: 物品id
    :param stuff_num: 数量
    :param is_bind: 是否已经绑定
    :param is_wearing: 是否穿戴中
    :param position_in_bag: 在背包中的位置，从1开始，目前没有设定背包大小。
    如果穿戴中，则其在背包中的位置属性没有意义。从穿戴到背包的时候会分配新的位置。
    :param current_stars_num: 当前升星数量
    :return: PlayerStuffRecord
    """
    record = PlayerStuffRecord(
        character_id=character_id,
        stuff_id=stuff_id,
        stuff_num=stuff_num,
        is_bind=is_bind,
        is_wearing=is_wearing,
        position_in_bag=position_in_bag,

        current_stars_num=current_stars_num,
    )
    session.add(record)
    session.commit()
    return record


# 删

# 改
def update_bag_stuffs_position(*,
                               stuff_position_list: List[PlayerStuffRecord, int]
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

def get_player_stuff_record_by_record_id(*,
                                         record_id: int
                                         ) -> PlayerStuffRecord:
    """
    根据 id 查询 player_stuff_record 记录
    :param record_id: 记录的 id
    :return: PlayerStuffRecord 对象
    """
    record = session.query(PlayerStuffRecord).filter_by(id=record_id).first()
    return record


def get_all_wearing_stuffs_by_character_id(*,
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
                                ):
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
    player_stuff_record = get_player_stuff_record_by_record_id(record_id=stuff_record_id)

    record = add_player_stuff_record(
        character_id=character_id,
        stuff_id=player_stuff_record.stuff_id,
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
                         ):
    """
    玩家穿着的物品放到背包中；
    :param character_id:
    :param player_stuff_record_id:
    :return:
    """
    available_position = get_min_unused_bag_position(
        character_id=character_id,
    )
    update_stuff_wearing_and_position(stuff_record_id=player_stuff_record_id,
                                      is_wearing=False,
                                      new_position=available_position)
    session.commit()


def bag_stuff_to_wearing(*,
                         player_stuff_record_id: int
                         ):
    """

    :param player_stuff_record_id:
    :return:
    """
    update_stuff_wearing_and_position(stuff_record_id=player_stuff_record_id,
                                      is_wearing=False)
    session.commit()
