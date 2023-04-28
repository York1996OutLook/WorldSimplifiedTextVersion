from typing import List, Optional

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean


from DBHelper.session import session
from DBHelper.tables.base_table import Basic,Base


class PlayerSkillRecord(Basic,Base):
    """
    已学习技能表。只存储最大等级。可能会被更新;
    """
    __tablename__ = 'player_skill_record'

    character_id = Column(Integer, comment="character_id")

    skill_id = Column(Integer, comment="技能ID")

    skill_level = Column(Integer, comment="已经学习的技能等级")
    learning_timestamp = Column(Integer, comment="学习的时间")

    @classmethod
    def add_or_update_by_ids(cls,
                             *,
                             _id: int = None,
                             character_id: int = None,
                             skill_id: int = None,
                             skill_level: int = None,
                             learning_timestamp: int = None
                             ):
        """
        更新或创建技能学习记录
        :param _id: 记录ID
        :param character_id: 人物ID
        :param skill_id: 技能ID
        :param skill_level: 已学习技能等级
        :param learning_timestamp: 学习时间
        :return:
        """
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_ids)
        record = cls._add_or_update_by_id(**fields)
        return record

# 删


# 改
def update_by_character_id_skill_id(*,
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



def update_level_by_record_id(*,
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
def get_by_character_id_and_skill_id(
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


def get_all_by_character_id(
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
