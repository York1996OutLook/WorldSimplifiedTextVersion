from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

Base = declarative_base()

engine = create_engine("sqlite:///mydatabase.db")
Session = sessionmaker(bind=engine)
session = Session()


class LearnedSkillRecord(Base):
    """
    已学习技能表
    """
    __tablename__ = 'learned_skill_record'

    id = Column(Integer, primary_key=True)

    player_id = Column(Integer, comment="玩家ID，qq号")

    skill_id = Column(Integer, comment="技能ID")  # ForeignKey(Skill.id)

    skill_level_id = Column(Integer, comment="已经学习的技能等级")
    learning_time = Column(Integer, comment="学习的时间")


# 增
def add_learned_skill_record(player_id: int, skill_id: int, skill_level_id: int, learning_time: int):
    """
    新增一个已经学习的技能记录
    """
    new_learned_skill_record = LearnedSkillRecord(player_id=player_id, skill_id=skill_id, skill_level_id=skill_level_id,
                                                  learning_time_id=learning_time)
    session.add(new_learned_skill_record)
    session.commit()


# 删
def delete_learned_skill_record_bt_skill_record_id(skill_record_id: int):
    """
    删除已学习技能记录
    :param skill_record_id: 记录的ID
    :return: None
    """
    session.query(LearnedSkillRecord).filter(LearnedSkillRecord.id == skill_record_id).delete()
    session.commit()


# 改
def update_learned_skill_record_by_player_id_skill_id(player_id: int, skill_id: int, new_skill_level_id: int,
                                new_learning_time_id: int) -> None:
    """
    更新已学习技能记录

    :param player_id: 玩家ID
    :param skill_id: 技能ID
    :param new_skill_level_id: 新的技能等级ID
    :param new_learning_time_id: 新的学习时间ID
    """
    record = session.query(LearnedSkillRecord).filter(LearnedSkillRecord.player_id == player_id,
                                                      LearnedSkillRecord.skill_id == skill_id).first()
    if record:
        record.skill_level_id = new_skill_level_id
        record.learning_time_id = new_learning_time_id
        session.commit()


def update_learned_skill_record_by_id(record_id: int, player_id: int, skill_id: int, skill_level_id: int,
                                      learning_time_id: int):
    """
    根据已学习技能记录的id进行修改
    :param record_id: 记录id
    :param player_id: 玩家id
    :param skill_id: 技能id
    :param skill_level_id: 已经学习的技能等级id
    :param learning_time_id: 学习的时间id
    :return: None
    """
    record = session.query(LearnedSkillRecord).filter(LearnedSkillRecord.id == record_id).first()
    if record is None:
        return None
    record.player_id = player_id
    record.skill_id = skill_id
    record.skill_level_id = skill_level_id
    record.learning_time_id = learning_time_id
    session.commit()


# 查

def query_learned_skill_record_by_player_id_or_skill_id(player_id: int = None, skill_id: int = None):
    """查询已学习技能记录

    Args:
        player_id (dict): 查询条件，比如 player_id=1， skill_id=2
        skill_id (dict): 查询条件，比如 player_id=1， skill_id=2
    """
    query = session.query(LearnedSkillRecord)
    if player_id is not None:
        query = query.filter(LearnedSkillRecord.player_id == player_id)
    if skill_id is not None:
        query = query.filter(LearnedSkillRecord.skill_id == skill_id)
    return query.all()
