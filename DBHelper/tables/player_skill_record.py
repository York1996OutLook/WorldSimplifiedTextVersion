from typing import List, Optional

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

Base = declarative_base()

from DBHelper.session import session


class PlayerSkillRecord(Base):
    """
    已学习技能表。只存储最大等级。可能会被更新；
    """
    __tablename__ = 'player_skill_record'

    id = Column(Integer, primary_key=True)

    character_id = Column(Integer, comment="character_id")  # 参考人物表

    skill_id = Column(Integer, comment="技能ID")  # ForeignKey(Skill.id)

    skill_level = Column(Integer, comment="已经学习的技能等级")
    learning_timestamp = Column(Integer, comment="学习的时间")


# 增
def add_player_skill_record(*,
                            character_id: int,
                            skill_id: int,
                            skill_level: int,
                            learning_timestamp: int):
    """
    新增一个已经学习的技能记录
    """
    player_skill_record = PlayerSkillRecord(character_id=character_id,
                                            skill_id=skill_id,
                                            skill_level=skill_level,
                                            learning_timestamp_id=learning_timestamp)
    session.add(player_skill_record)
    session.commit()
    return player_skill_record


# 删
def delete_learned_skill_record_bt_skill_record_id(*,
                                                   skill_record_id: int):
    """
    删除已学习技能记录
    :param skill_record_id: 记录的ID
    :return: None
    """
    session.query(PlayerSkillRecord).filter(PlayerSkillRecord.id == skill_record_id).delete()
    session.commit()


# 改
def update_learned_skill_record_by_character_id_skill_id(*,
                                                         character_id: int,
                                                         skill_id: int,
                                                         new_skill_level: int,
                                                         new_learning_timestamp: int) -> None:
    """
    更新已学习技能记录

    :param character_id: character_id
    :param skill_id: 技能ID
    :param new_skill_level: 新的技能等级ID
    :param new_learning_timestamp: 新的学习时间
    """
    record = session.query(PlayerSkillRecord).filter(PlayerSkillRecord.character_id == character_id,
                                                     PlayerSkillRecord.skill_id == skill_id).first()
    record.skill_level = new_skill_level
    record.learning_timestamp = new_learning_timestamp
    session.commit()


def update_learned_skill_record_by_character_id(*,
                                                record_id: int,
                                                character_id: int,
                                                skill_id: int,
                                                skill_level: int,
                                                learning_timestamp: int):
    """
    根据已学习技能记录的id进行修改
    :param record_id: 记录id
    :param character_id: character_id
    :param skill_id: 技能id
    :param skill_level: 已经学习的技能等级id
    :param learning_timestamp: 学习的时间
    :return: None
    """
    record = session.query(PlayerSkillRecord).filter(PlayerSkillRecord.id == record_id).first()
    record.character_id = character_id
    record.skill_id = skill_id
    record.skill_level = skill_level
    record.learning_timestamp = learning_timestamp
    session.commit()


def update_player_skill_record_level_by_character_id(*,
                                                     record_id: int,
                                                     skill_level: int,
                                                     learning_timestamp: int):
    """
    根据已学习技能记录的id进行修改等級
    :param record_id: 记录id
    :param skill_level: 已经学习的技能等级id
    :param learning_timestamp: 学习的时间
    :return: None
    """
    record = session.query(PlayerSkillRecord).filter(PlayerSkillRecord.id == record_id).first()
    record.skill_level = skill_level
    record.learning_timestamp = learning_timestamp
    session.commit()


# 查
def get_player_skill_record_by_character_id_and_skill_id(
        *,
        character_id: int,
        skill_id: int
) -> PlayerSkillRecord:
    """查询已学习技能记录

    Args:
        character_id (int): 查询条件，比如 character_id=1
        skill_id (int): 查询条件，比如 character_id=1
    """
    query = session.query(PlayerSkillRecord)
    query = query.filter(PlayerSkillRecord.character_id == character_id, skill_id == skill_id)
    return query.first()


def get_player_all_skill_record_by_character_id(
        *,
        character_id: int,
) -> List[PlayerSkillRecord]:
    """查询已学习技能记录

    Args:
        character_id (int): 查询条件，比如 character_id=1
    """
    query = session.query(PlayerSkillRecord)
    query = query.filter(PlayerSkillRecord.character_id == character_id)
    return query.all()
