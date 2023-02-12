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

    skill_name = Column(String, comment="技能名称")
    is_positive = Column(Boolean, comment="是否是主动技能，如果是主动技能则需要设置何时释放")
    effect_expression = Column(String, comment="效果说明")


# 增
def add_skill(*,
              skill_name: str,
              is_positive: bool,
              effect_expression: str
              ) -> Skill:
    """
    Add a new skill to the 'skill' table.

    Args:
        skill_name (str): The name of the new skill.
        is_positive (bool): Whether the new skill is a positive skill or not.
        effect_expression (str): The effect expression of the new skill.
    """
    # Create a new skill
    new_skill = Skill(skill_name=skill_name, is_positive=is_positive, effect_expression=effect_expression)

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

    # If the skill with the specified ID exists
    if skill:
        # Delete the skill from the session
        session.delete(skill)

        # Commit the transaction
        session.commit()
# 改

# 查
