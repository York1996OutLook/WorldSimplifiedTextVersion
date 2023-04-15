from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from typing import List

Base = declarative_base()

from DBHelper.session import session


class Skill(Base):
    """
    人物可学习或者怪物的技能
    """
    __tablename__ = 'skill'
    id = Column(Integer, primary_key=True)
    in_skill_store = Column(Boolean, comment="是否可以直接进行学习，如果能的话代表能够在技能所学习，否则可能是装备附带的技能。")
    skill_name = Column(String, comment="技能名称")
    is_positive = Column(Boolean, comment="是否是主动技能，如果是主动技能则需要设置何时释放")
    target = Column(Integer, comment="")
    effect_expression = Column(String, comment="效果说明")

    def __init__(self, *, in_skill_store: bool, skill_name: str, is_positive: bool, effect_expression: str):
        self.in_skill_store = in_skill_store
        self.skill_name = skill_name
        self.is_positive = is_positive
        self.effect_expression = effect_expression


# 增
def add(*,
        skill_name: str,
        in_skill_store: bool,
        is_positive: bool,
        effect_expression: str
        ) -> Skill:
    """
    Add a new skill to the 'skill' table.

    Args:
        skill_name (str): The name of the new skill.
        in_skill_store (bool):
        is_positive (bool): Whether the new skill is a positive skill or not.
        effect_expression (str): The effect expression of the new skill.
    """
    # Create a new skill
    new_skill = Skill(skill_name=skill_name,
                      in_skill_store=in_skill_store,
                      is_positive=is_positive,
                      effect_expression=effect_expression)

    # Add the new skill to the session
    session.add(new_skill)

    # Commit the transaction
    session.commit()
    return new_skill


# 删
def delete_skill(*,
                 skill_id: int
                 ):
    """
    Delete a skill from the 'skill' table based on its ID.

    Args:
        skill_id (int): The ID of the skill to be deleted.
    """
    # Get the skill with the specified ID
    skill = session.query(Skill).filter_by(id=skill_id).first()

    # Delete the skill from the session
    session.delete(skill)

    # Commit the transaction
    session.commit()


# 改
def update_name_by_id(*, _id: int, name: str) -> Skill:
    record = session.query(Skill).filter(Skill.id == _id).first()
    record.skill_name = name
    session.commit()
    return record


# 查
def get_by_name(*, name: str) -> Skill:
    record = session.query(Skill).filter(Skill.skill_name == name).first()
    return record

def is_exists_by_name(*,name:str)->Skill:
    record = session.query(Skill).filter(Skill.skill_name == name).first()
    return record is not None


def get_all() -> List[Skill]:
    """
    获取所有的skill
    :return:
    """
    skills = session.query(Skill).all()
    return skills
