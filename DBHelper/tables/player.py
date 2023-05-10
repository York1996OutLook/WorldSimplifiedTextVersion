from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Float, Boolean
from typing import Optional, List

Base = declarative_base()

from DBHelper.session import session
from DBHelper.tables.base_table import CustomColumn,Timestamp
from DBHelper.tables.base_table import Entity


class Player(Entity, Base):
    """
    人物属性表
    """
    __cn__ = "玩家"
    __tablename__ = 'player'

    name = CustomColumn(String, cn="昵称", comment='昵称(QQ昵称),不唯一!')
    player_id = CustomColumn(Integer, cn="QQ", comment="QQ")

    first_login_timestamp = CustomColumn(Timestamp, cn="第一次登陆时间", comment="第一次登录的时间戳")

    current_level = CustomColumn(Integer,cn="当前等级", comment='当前等级')
    current_experience = CustomColumn(Integer, cn="当前经验值",comment='当前经验值,为当前经验值')

    game_sign = CustomColumn(String, cn="游戏签名",comment="游戏中的签名,可以被其他角色查看到属性")

    gold_num = CustomColumn(Integer, cn="黄金数量",comment="黄金数量,游戏唯一游戏币")

    achievement_id = CustomColumn(Integer,cn="佩戴称号ID", comment="成就id")

    @classmethod
    def add_or_update_by_id(cls,
                            *,
                            _id: int = None,
                            name: str = None,
                            player_id: int = None,
                            first_login_timestamp: int = None,
                            current_level: int = None,
                            current_experience: int = None,
                            game_sign: str = None,
                            gold_num: int = None,
                            achievement_id: int = None
                            ):
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
        return record

    @classmethod
    def add_or_update_by_name(cls,
                              *,
                              name: str,
                              player_id: int = None,
                              first_login_timestamp: int = None,
                              current_level: int = None,
                              current_experience: int = None,
                              game_sign: str = None,
                              gold_num: int = None,
                              achievement_id: int = None
                              ) -> "Player":
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_name)
        record = cls._add_or_update_by_name(**fields)
        return record


# 删
def delete_by_player_id(*, player_id: int) -> None:
    """
    根据player_id删除人物

    :param player_id: 人物的id
    :return: None
    """
    player = session.query(Player).filter(Player.player_id == player_id).first()
    session.delete(player)
    session.commit()


# 改
def update_player(*,
                  character_id: int,
                  nickname: Optional[str] = None,
                  current_level: Optional[int] = None,
                  current_experience: Optional[int] = None,
                  game_sign: Optional[str] = None,
                  achievement_id: int = None
                  ) -> Player:
    """
    更新人物属性
    :param character_id: 人物ID
    :param nickname: 昵称
    :param current_level: 当前等级
    :param current_experience: 当前经验值
    :param game_sign: 游戏中的签名
    :param pk_rank: pk排名名次
    :param achievement_id: pk排名名次
    :return: None
    """
    player = session.query(Player).filter(Player.id == character_id).first()
    if nickname is not None:
        player.nickname = nickname
    if current_level is not None:
        player.current_level = current_level
    if current_experience is not None:
        player.current_experience = current_experience
    if game_sign is not None:
        player.game_sign = game_sign
    if achievement_id is None:
        player.achievement_id = achievement_id
    session.commit()
    session.refresh(player)
    return player


def update_achievement_id(*,
                          character_id: int,
                          achievement_id: int,
                          ) -> Player:
    """
    更新人物属性
    :param character_id: 人物ID
    :param achievement_id: pk排名名次
    :return: None
    """
    player = session.query(Player).filter(Player.id == character_id).first()
    player.achievement_id = achievement_id
    session.commit()
    session.refresh(player)


# 查
def is_exists_by_player_id(*, player_id: int) -> bool:
    """
    检查玩家是否存在

    Args:
        player_id: 玩家ID

    Returns:
        bool: 如果玩家存在返回 True，否则返回 False

    Raises:
        NoResultFound: 当查询不到结果时，抛出异常
    """
    player = session.query(Player).filter_by(player_id=player_id).first()
    return player is not None


def get_by_player_id(*, player_id: int) -> Player:
    """
    根据人物ID查询人物信息

    :param player_id: 人物ID
    :return: Player对象
    """
    player = session.query(Player).filter_by(player_id=player_id).first()
    return player


def get_by_character_id(*, character_id: int) -> Player:
    """
    根据人物ID查询人物信息

    :param character_id: 人物ID
    :return: Player对象
    """
    player = session.query(Player).filter_by(id=character_id).first()
    return player
