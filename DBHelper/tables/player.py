from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean
from typing import Optional, List

Base = declarative_base()

from DBHelper.session import session


class Player(Base):
    """
    人物属性表
    """
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True, comment='ID')
    player_id = Column(Integer, comment="QQ")
    nickname = Column(String, comment='昵称（QQ昵称）')

    first_login_timestamp = Column(Integer, comment="第一次登录的时间戳")

    current_level = Column(Integer, comment='当前等级')
    current_experience = Column(Integer, comment='当前经验值，为当前经验值')

    game_sign = Column(String, comment="游戏中的签名，可以被其他角色查看到属性")

    gold_num = Column(Integer, comment="黄金数量，游戏唯一游戏币")

    pk_rank = Column(Integer, comment="pk排名次")
    achievement_id = Column(Integer, comment="成就id")


# 增
def add_player(*,
               player_id: int,
               nickname: str,
               current_level: int,
               game_sign: str
               ) -> Player:
    """
    新增玩家记录
    :param player_id: qq
    :param nickname: 昵称（QQ昵称）
    :param current_level: 昵称（QQ昵称）
    :param game_sign: 昵称（QQ昵称）
    :return:
    """
    player = Player(player_id=player_id,
                    nickname=nickname,
                    current_level=current_level,
                    current_experience=0,
                    game_sign=game_sign,
                    pk_rank=0,
                    gold_num=0,
                    )
    session.add(player)
    session.commit()
    return player


# 删
def delete_player_by_player_id(*, player_id: int) -> None:
    """
    根据player_id删除人物

    :param player_id: 人物的id
    :return: None
    """
    player = session.query(Player).filter(Player.player_id == player_id).first()
    session.delete(player)
    session.commit()


def delete_player_by_id(*, character_id: int) -> None:
    """
    根据player_id删除人物

    :param character_id: 人物的id，非player ID
    :return: None
    """
    player = session.query(Player).filter(Player.id == character_id).first()
    session.delete(player)
    session.commit()


# 改


def update_player(*,
                  character_id: int,
                  nickname: Optional[str] = None,
                  current_level: Optional[int] = None,
                  current_experience: Optional[int] = None,
                  game_sign: Optional[str] = None,
                  pk_rank: Optional[int] = None,
                  achievement_id: int = None
                  ):
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
    if pk_rank is not None:
        player.pk_rank = pk_rank
    if achievement_id is None:
        player.achievement_id = achievement_id
    session.commit()


def update_player_achievement_id(*,
                                 character_id: int,
                                 achievement_id: int,
                                 ):
    """
    更新人物属性
    :param character_id: 人物ID
    :param achievement_id: pk排名名次
    :return: None
    """
    player = session.query(Player).filter(Player.id == character_id).first()
    player.achievement_id = achievement_id
    session.commit()


# 查
def is_player_exists_by_player_id(*, player_id: int) -> bool:
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


def get_player_by_player_id(*, player_id: int) -> Player:
    """
    根据人物ID查询人物信息

    :param player_id: 人物ID
    :return: Player对象
    """
    player = session.query(Player).filter_by(player_id=player_id).first()
    return player


def get_player_by_character_id(*, character_id: int) -> Player:
    """
    根据人物ID查询人物信息

    :param character_id: 人物ID
    :return: Player对象
    """
    player = session.query(Player).filter_by(id=character_id).first()
    return player


def query_player_by_nickname(*, nickname: str) -> Player:
    """
    根据昵称查询人物信息

    :param nickname: 人物昵称
    :return: Player对象
    """
    player = session.query(Player).filter_by(nickname=nickname).first()
    return player


def query_player_by_level(*, level: int) -> List[Player]:
    """
    根据等级查询人物信息
    :param level: 等级
    :return: 人物信息列表
    """
    result = session.query(Player).filter(Player.current_level == level).all()
    return result
