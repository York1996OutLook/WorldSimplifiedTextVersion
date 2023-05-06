from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from typing import List

from Enums import LearningApproach, SkillTarget, SkillType

Base = declarative_base()

from DBHelper.session import session

from DBHelper.tables.base_table import Entity


class Skill(Entity,Base):
    """
    人物可学习或者怪物的技能
    """
    __tablename__ = 'skill'
    learning_approach = Column(Integer, default=LearningApproach.IN_SKILL_ACADEMY.index,
                               comment="是否可以直接进行学习,如果能的话代表能够在技能所学习,否则可能是装备附带的技能。")
    skill_type = Column(Integer, default=SkillType.PASSIVE.index, comment="技能类型")
    target = Column(Integer, default=SkillTarget.SELF.index, comment="技能的作用对象")
    effect_expression = Column(String, comment="效果说明")

    @classmethod
    def add_or_update_by_name(cls,
                              *,
                              name: str,
                              learning_approach: int = None,
                              skill_type: int = None,
                              target: int = None,
                              effect_expression: str = None
                              ) -> "Skill":
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_name)
        record = cls._add_or_update_by_name(**fields)
        return record

    @classmethod
    def add_or_update_by_id(
            cls,
            *,
            _id: int,

            name: str = None,
            learning_approach: int = None,
            skill_type: int = None,
            target: int = None,
            effect_expression: str = None
    ) -> "Skill":
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
        return record

# 增

# 删

# 改

# 查
