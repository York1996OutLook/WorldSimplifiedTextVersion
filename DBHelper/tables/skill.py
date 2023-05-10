from sqlalchemy import Integer, String, Boolean,Text
from sqlalchemy.ext.declarative import declarative_base
from typing import List

from DBHelper.tables.base_table import CustomColumn
from Enums import LearningApproach, SkillTarget, SkillType

Base = declarative_base()

from DBHelper.session import session

from DBHelper.tables.base_table import Entity


class Skill(Entity, Base):
    """
    人物可学习或者怪物的技能
    """
    __cn__ = "技能"
    __tablename__ = 'skill'
    name = CustomColumn(String, cn='名称')  # 显式复制并设置 cn 属性

    learning_approach = CustomColumn(Integer, bind_type=LearningApproach,
                                     cn="学习途径", comment="是否可以直接进行学习,如果能的话代表能够在技能所学习,否则可能是装备附带的技能。")
    skill_type = CustomColumn(Integer, cn="技能类型", bind_type=SkillType, comment="技能类型")
    target = CustomColumn(Integer, cn="作用对象", bind_type=SkillTarget, comment="技能的作用对象")
    effect_expression = CustomColumn(Text, cn="效果说明", comment="效果说明")

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
