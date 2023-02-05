from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

from typing import Optional,List

Base = declarative_base()

engine = create_engine("sqlite:///mydatabase.db")
Session = sessionmaker(bind=engine)
session = Session()


class Player(Base):
    """
    人物属性表
    """
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True, comment='ID,qq号')
    nickname = Column(String, comment='昵称（QQ昵称）')
    current_level = Column(Integer, comment='当前等级')
    current_experience = Column(Integer, comment='当前经验值，为当前经验值')
    attack_property = Column(Integer, comment="参考攻击属性表")
    game_sign = Column(String, comment="游戏中的签名，可以被其他玩家查看到属性")

# 增
def add_player(nickname: str, current_level: int, current_experience: int, attack_property: int, game_sign: str):
    """
    新增玩家记录
    :param nickname: 昵称（QQ昵称）
    :param current_level: 当前等级
    :param current_experience: 当前经验值
    :param attack_property: 参考攻击属性表
    :param game_sign: 游戏中的签名
    :return:
    """
    player = Player(nickname=nickname, current_level=current_level, current_experience=current_experience,
                    attack_property=attack_property, game_sign=game_sign)
    session.add(player)
    session.commit()

# 删
def delete_player_by_id(session, player_id: int) -> None:
    """
    根据playerid删除人物

    :param session: 数据库会话
    :param player_id: 人物的id
    :return: None
    """
    player = session.query(Player).filter(Player.id == player_id).first()
    if player:
        session.delete(player)
        session.commit()


# 改
def update_player(session, player_id: int, nickname: Optional[str]=None, current_level: Optional[int]=None, current_experience: Optional[int]=None, attack_property: Optional[int]=None, game_sign: Optional[str]=None):
    """
    更新人物属性
    :param session: SQLAlchemy的session
    :param player_id: 人物ID
    :param nickname: 昵称
    :param current_level: 当前等级
    :param current_experience: 当前经验值
    :param attack_property: 攻击属性
    :param game_sign: 游戏中的签名
    :return: None
    """
    player = session.query(Player).filter(Player.id == player_id).first()
    if player is None:
        return
    if nickname is not None:
        player.nickname = nickname
    if current_level is not None:
        player.current_level = current_level
    if current_experience is not None:
        player.current_experience = current_experience
    if attack_property is not None:
        player.attack_property = attack_property
    if game_sign is not None:
        player.game_sign = game_sign
    session.commit()


# 查
def query_player_by_id(player_id: int) -> Player:
    """
    根据人物ID查询人物信息

    :param player_id: 人物ID
    :return: Player对象
    """
    player = session.query(Player).filter_by(id=player_id).first()
    return player

def query_player_by_nickname(nickname: str) -> Player:
    """
    根据昵称查询人物信息

    :param nickname: 人物昵称
    :return: Player对象
    """
    player = session.query(Player).filter_by(nickname=nickname).first()
    return player



def query_player_by_level(level: int) -> List[Player]:
    """
    根据等级查询人物信息
    :param level: 等级
    :return: 人物信息列表
    """
    result = session.query(Player).filter(Player.current_level == level).all()

    session.close()
    return result

