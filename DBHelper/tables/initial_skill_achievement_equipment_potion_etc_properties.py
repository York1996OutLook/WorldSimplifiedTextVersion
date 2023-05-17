from collections import defaultdict
from typing import Optional, DefaultDict, List

from sqlalchemy import Integer, String, Boolean

from DBHelper.session import session
from DBHelper.tables.base_table import CustomColumn

from DBHelper.tables.base_table import Basic, Base
from Enums import AdditionSourceType, AdditionalPropertyType, PropertyAvailability, StuffType


class InitialSkillAchievementEquipmentPotionEtcPropertiesRecord(Basic, Base):
    """初始属性，基础属性加点、技能、装备(最大，最小，当前)、称号，临时药剂等常见的所有属性表，为永久表"""
    __tablename__ = 'initial_skill_achievement_equipment_etc_properties_record'
    id = CustomColumn(Integer, cn="ID", primary_key=True, editable=False,autoincrement=True)

    additional_source_type = CustomColumn(Integer, cn="属性", bind_type=AdditionSourceType,
                                          comment="带来属性提升的物品类型，比如成就初始属性，基础属性加点，称号，技能，装备.参考枚举类型 AdditionSourceType")
    additional_source_id = CustomColumn(Integer, cn="物品ID", comment="""
带来属性提升的物品id。
如果是初始属性，则此项为空。
如果基础属性，则此项为character id。
如果是称号，则此项为achievement_id。
如果是技能，则此项为skill_book_id。
如果是装备，则此项为stuff_record_id。
如果是药剂，则此项为potion_id。
如果是状态，则此项为status_id。
    """)  # todo

    additional_source_property_index = CustomColumn(Integer, cn='属性索引', comment="""
带来属性提升的属性索引。

如果是初始属性，则该项为0。
如果基础属性，则此项为0。
如果是称号，则此项为1 2 3...。
如果是技能，则此项为1 2 3...。
如果是装备，则此项为1 2 3...。
如果是药剂，则此项为1 2 3...。
如果是状态，则此项为1 2 3...。
    """)
    property_availability = CustomColumn(Integer,
                                         cn="作用域",
                                         bind_type=PropertyAvailability,
                                         comment="属性的类型，参考PropertyAvailability。"
                                                 "对于装备来说：表明是最低属性，最高属性还是当前属性"
                                                 "对于技能来说，这个属性为作用的对象，自身或者是敌人")

    additional_property_type = CustomColumn(Integer, cn="属性", bind_type=AdditionalPropertyType,
                                            comment="参考AdditionalPropertyType")
    additional_property_value = CustomColumn(Integer, cn="属性值", comment="对应参考AdditionalPropertyType的value")

    @classmethod
    def add_or_update_by_id(cls,
                            *,
                            _id: int,
                            additional_source_type: int = None,

                            additional_property_type: int = None,
                            additional_property_value: int = None,

                            additional_source_id: int = None,
                            additional_source_property_index: int = None,

                            property_availability: int = None,
                            ) -> "InitialSkillAchievementEquipmentPotionEtcPropertiesRecord":
        property_record = cls._add_or_update_by_id(kwargs=locals())
        return property_record

    @classmethod
    def get_properties_by_skill_book_id(cls,
                                        *,
                                        skill_book_id: int,
                                        ) -> List["InitialSkillAchievementEquipmentPotionEtcPropertiesRecord"]:
        properties_record = cls.get_properties_by(additional_source_type=AdditionSourceType.SKILL_BOOK.index,
                                                  additional_source_id=skill_book_id)
        return properties_record

    # 增
    @classmethod
    def add(cls,
            additional_source_type: int = None,
            additional_source_id: int = None,

            additional_property_type: int = None,
            additional_property_value: int = None,

            additional_source_property_index: int = None,

            property_availability: int = None,
            ) -> 'InitialSkillAchievementEquipmentPotionEtcPropertiesRecord':
        property_record = cls.add_with_kwargs(kwargs=locals())
        return property_record

    @classmethod
    def add_player_properties(cls,
                              *,
                              character_id: int,
                              additional_property_type: int,
                              additional_property_value: int,
                              ) -> 'InitialSkillAchievementEquipmentPotionEtcPropertiesRecord':
        property_record = cls.add(additional_source_type=AdditionSourceType.PLAYER.index,
                                  additional_source_id=character_id,
                                  additional_property_type=additional_property_type,
                                  additional_property_value=additional_property_value,
                                  )
        return property_record

    @classmethod
    def add_initial_properties(cls,
                               *,
                               additional_property_type: int,
                               additional_property_value: int,
                               ) -> 'InitialSkillAchievementEquipmentPotionEtcPropertiesRecord':
        property_record = cls.add(additional_source_type=AdditionSourceType.INITIAL.index,
                                  additional_property_type=additional_property_type,
                                  additional_property_value=additional_property_value,
                                  )
        return property_record

    @classmethod
    def add_monster_properties(cls,
                               *,
                               monster_id: int,
                               additional_property_type: int,
                               additional_property_value: int,
                               ) -> 'InitialSkillAchievementEquipmentPotionEtcPropertiesRecord':
        property_record = cls.add(additional_source_type=AdditionSourceType.MONSTER.index,
                                  additional_source_id=monster_id,
                                  additional_property_type=additional_property_type,
                                  additional_property_value=additional_property_value,
                                  )
        return property_record

    @classmethod
    def add_base_additional_properties(cls,
                                       *,
                                       base_property_type: int,
                                       additional_source_property_index: int,
                                       additional_property_type: int,
                                       additional_property_value: int
                                       ) -> 'InitialSkillAchievementEquipmentPotionEtcPropertiesRecord':
        """

        :param base_property_type: 基础属性值。作为additional_source_id存到表格中；
        :param additional_source_property_index: 属性索引
        :param additional_property_type: 基础属性增加的其它的额外属性
        :param additional_property_value: 其它额外属性的值
        :return:
        """
        property_record = cls.add(additional_source_type=AdditionSourceType.BASE_ADDITIONAL.index,
                                  additional_source_id=base_property_type,
                                  additional_source_property_index=additional_source_property_index,
                                  additional_property_type=additional_property_type,
                                  additional_property_value=additional_property_value,
                                  )
        return property_record

    @classmethod
    def add_equipment_properties(cls,
                                 *,
                                 equipment_stuff_id: int,
                                 additional_source_property_index: int,

                                 property_availability: int = None,
                                 additional_property_type: int = None,
                                 additional_property_value: int = None,
                                 ) -> 'InitialSkillAchievementEquipmentPotionEtcPropertiesRecord':
        property_record = cls.add(additional_source_type=AdditionSourceType.EQUIPMENT_PROTOTYPE.index,
                                  additional_source_id=equipment_stuff_id,
                                  additional_source_property_index=additional_source_property_index,
                                  property_availability=property_availability,
                                  additional_property_type=additional_property_type,
                                  additional_property_value=additional_property_value,
                                  )
        return property_record

    @classmethod
    def add_achievement_properties(cls,
                                   *,
                                   achievement_id: int,
                                   additional_source_property_index: int,
                                   additional_property_type: int,
                                   additional_property_value: int,
                                   ) -> 'InitialSkillAchievementEquipmentPotionEtcPropertiesRecord':
        property_record = cls.add_with_kwargs(additional_source_type=AdditionSourceType.ACHIEVEMENT_TITLE.index,
                                              additional_source_id=achievement_id,
                                              additional_source_property_index=additional_source_property_index,
                                              additional_property_type=additional_property_type,
                                              additional_property_value=additional_property_value,
                                              )
        return property_record

    # 删
    @classmethod
    def del_by_additional_source_type_id(cls,
                                         *,
                                         additional_source_type: int,
                                         additional_source_id: int = None,
                                         ):

        is_del_data = cls.del_all_by_kwargs(kwargs=locals())
        return is_del_data

    @classmethod
    def del_initial_properties(cls) -> bool:
        """
        删除成就对应的所有属性加成
        :return:
        """
        is_del_data = cls.del_all_by_kwargs(additional_source_type=AdditionSourceType.INITIAL.index)
        return is_del_data

    @classmethod
    def del_achievement_properties(cls,
                                   *,
                                   achievement_id: int = None,
                                   ) -> bool:
        """
        删除成就对应的所有属性加成
        :param achievement_id:
        :return:
        """
        is_del_data = cls.del_all_by_kwargs(additional_source_type=AdditionSourceType.ACHIEVEMENT_TITLE.index,
                                            additional_source_id=achievement_id)
        return is_del_data

    @classmethod
    def del_equipment_prototype_properties(cls,
                                           *,
                                           equipment_id: int,
                                           ) -> bool:
        """
        删除某个装备原型的所有属性。
        :param equipment_id:
        :return:
        """
        is_del_data = cls.del_all_by_kwargs(additional_source_type=AdditionSourceType.EQUIPMENT_PROTOTYPE.index,
                                            additional_source_id=equipment_id)
        return is_del_data

    @classmethod
    def del_monster_prototype_properties(cls,
                                         *,
                                         monster_id: int,
                                         ) -> bool:
        """
        删除某个装备原型的所有属性。
        :param monster_id:
        :return:
        """
        is_del_data = cls.del_all_by_kwargs(additional_source_type=AdditionSourceType.MONSTER.index,
                                            additional_source_id=monster_id)
        return is_del_data

    @classmethod
    def del_skill_book_properties(cls,
                                  *,
                                  skill_book_id: int,
                                  ) -> bool:
        """
        删除某个装备原型的所有属性。
        :param skill_book_id:
        :return:
        """

        is_del_data = cls.del_all_by_kwargs(additional_source_type=AdditionSourceType.SKILL_BOOK.index,
                                            additional_source_id=skill_book_id)
        return is_del_data

    @classmethod
    def del_status_properties(cls,
                              *,
                              status_id: int,
                              ) -> bool:
        """
        删除某个装备原型的所有属性。
        :param status_id:
        :return:
        """
        is_del_data = cls.del_all_by_kwargs(additional_source_type=AdditionSourceType.STATUS.index,
                                            additional_source_id=status_id)
        return is_del_data

    @classmethod
    def del_base_additional_properties(cls,
                                       *,
                                       base_property_type: int,
                                       ) -> bool:
        is_del_data = cls.del_all_by_kwargs(additional_source_type=AdditionSourceType.BASE_ADDITIONAL.index,
                                            additional_source_id=base_property_type)
        return is_del_data

    # 改
    @classmethod
    def update_base_additional_properties(cls,
                                          *,
                                          base_property_type: int,
                                          additional_property_type: int,

                                          additional_property_value: int
                                          ) -> "InitialSkillAchievementEquipmentPotionEtcPropertiesRecord":
        query_dict = {
            'additional_source_type': AdditionSourceType.BASE_ADDITIONAL.index,
            'base_property_type': base_property_type,
            'additional_property_type': additional_property_type,
        }
        update_dict = {
            "additional_property_value": additional_property_value
        }
        property_record = cls.update_fields_by_query_dict(query_dict=query_dict, update_dict=update_dict)

        return property_record

    @classmethod
    def update_player_base_property_by(cls,
                                       *,
                                       character_id: int,
                                       base_property_type: int,
                                       base_property_value: int,
                                       ) -> 'InitialSkillAchievementEquipmentPotionEtcPropertiesRecord':
        """
        更新基础属性
        :param character_id:
        :param base_property_type:
        :param base_property_value:
        :return:
        """
        query_dict = {
            'additional_source_type': AdditionSourceType.BASE_PROPERTY_POINT.index,
            'additional_source_id': character_id,

            'additional_property_type': base_property_type,
        }
        update_dict = {
            "additional_property_value": base_property_value
        }
        property_record = cls.update_fields_by_query_dict(query_dict=query_dict, update_dict=update_dict)
        return property_record

    @classmethod
    def update_player_property(cls,
                               *,
                               character_id: int = None,

                               additional_property_type: int,
                               additional_property_value: int,
                               ) -> "InitialSkillAchievementEquipmentPotionEtcPropertiesRecord":
        query_dict = {
            'additional_source_type': AdditionSourceType.PLAYER.index,
            'additional_source_id': character_id,
            'additional_property_type': additional_property_type,
        }
        update_dict = {
            "additional_property_value": additional_property_value
        }
        property_record = cls.update_fields_by_query_dict(query_dict=query_dict, update_dict=update_dict)
        return property_record

    @classmethod
    def update_skill_property(cls,

                              *,
                              skill_id: int,
                              property_index: int,
                              additional_property_type: int,
                              additional_property_value: int,
                              ) -> 'InitialSkillAchievementEquipmentPotionEtcPropertiesRecord':
        """
        :param skill_id:    技能id
        :param property_index:  属性的id。第一条属性，第二条属性，第三条属性，第四条属性
        :param additional_property_type: 属性的类型
        :param additional_property_value:   属性值
        :return:
        """
        ...

    @classmethod
    def update_skill_book_property(cls,
                                   *,
                                   skill_book_id: int = None,
                                   property_index: int,
                                   property_target: int,
                                   additional_property_type: int,
                                   additional_property_value: int,
                                   ) -> 'InitialSkillAchievementEquipmentPotionEtcPropertiesRecord':
        """
        :param skill_book_id:    技能id
        :param property_index:  属性的id。第一条属性，第二条属性，第三条属性，第四条属性
        :param property_target: 属性的作用对象。对于被动技能来说，作用对象是自己，对于主动技能，作用对象可能是自己也可能是对方；
        :param additional_property_type: 属性的类型
        :param additional_property_value:   属性值
        :return:
        """
        ...

    @classmethod
    def update_player_properties_dict(cls,
                                      *,
                                      character_id: int = None,
                                      properties_dict: DefaultDict[int, int]
                                      ) -> 'InitialSkillAchievementEquipmentPotionEtcPropertiesRecord':
        """
        更新用户的属性
        :param character_id:
        :param properties_dict:
        :return:
        """
        ...

    # 查
    @classmethod
    def is_exists(cls,
                  *,
                  additional_source_type: int = None,
                  additional_source_id: int = None,
                  additional_source_property_index: int = None,
                  property_availability: int = None,
                  additional_property_type: int = None,
                  ) -> bool:
        is_exists = cls.is_exists_by_kwargs(kwargs=locals())
        return is_exists

    @classmethod
    def get_properties_by(cls,
                          *,
                          additional_source_type: int,
                          additional_source_id: int = None,

                          additional_source_property_index: int = None,
                          property_availability: PropertyAvailability = None,

                          additional_property_type: int = None,
                          ) -> List["InitialSkillAchievementEquipmentPotionEtcPropertiesRecord"]:
        property_records = cls.get_all_by_kwargs(kwargs=locals())
        return property_records

    # other
    @classmethod
    def get_properties_dict_by(cls,
                               *,
                               additional_source_type: int,
                               additional_source_id: int = None,

                               additional_source_property_index: int = None,
                               property_availability: PropertyAvailability = None,

                               additional_property_type: int = None,
                               ) -> DefaultDict[int, int]:
        properties_dict = defaultdict(int)

        properties = cls.get_properties_by(additional_source_type=additional_source_type,
                                           additional_source_id=additional_source_id,
                                           additional_source_property_index=additional_source_property_index,
                                           property_availability=property_availability,
                                           additional_property_type=additional_property_type,
                                           )
        for one_property in properties:
            properties_dict[one_property.additional_property_type] += one_property.additional_property_value

        return properties_dict

    @classmethod
    def get_properties_dict_by_initial(cls
                                       ) -> DefaultDict[int, int]:
        """
        获取初始属性。分开写函数，减少错误发生
        :return:
        """
        properties_dict = cls.get_properties_dict_by(additional_source_type=AdditionSourceType.INITIAL.index)
        return properties_dict

    @classmethod
    def get_properties_dict_by_achievement_id(cls,
                                              *,
                                              achievement_id: int,
                                              ) -> DefaultDict[int, int]:
        """
        获取成就称号对应的属性。分开写函数，减少错误发生
        :return:
        """
        properties_dict = cls.get_properties_dict_by(
            additional_source_type=AdditionSourceType.ACHIEVEMENT_TITLE.index,
            additional_source_id=achievement_id,
        )
        return properties_dict

    @classmethod
    def get_base_property_dict_by_character_id(cls,
                                               *,
                                               character_id: int,
                                               ) -> DefaultDict[int, int]:
        """
        获取基础属性对应的属性。分开写函数，减少错误发生
        :return:
        """
        properties_dict = cls.get_properties_dict_by(
            additional_source_type=AdditionSourceType.BASE_PROPERTY_POINT,
            additional_source_id=character_id,
        )
        return properties_dict

    @classmethod
    def get_property_dict_by_skill_id(cls,
                                      *,
                                      skill_id: int,
                                      ) -> DefaultDict[int, int]:
        """
        获取基础属性对应的属性。分开写函数，减少错误发生
        :return:
        """
        properties_dict = cls.get_properties_dict_by(
            additional_source_type=AdditionSourceType.SKILL.index,
            additional_source_id=skill_id,
        )
        return properties_dict

    @classmethod
    def get_property_dict_by_monster_id(cls,
                                        *,
                                        monster_id: int,
                                        ) -> DefaultDict[int, int]:
        """
        获取基础属性对应的属性。分开写函数，减少错误发生
        :return:
        """
        properties_dict = cls.get_properties_dict_by(
            additional_source_type=AdditionSourceType.MONSTER.index,
            additional_source_id=monster_id,
        )
        return properties_dict

    @classmethod
    def get_used_base_property_points_num_by_character_id(cls,
                                                          *,
                                                          character_id: int,
                                                          ) -> int:
        """
        获取已经使用的基础点数数量
        :param character_id:
        :return:
        """
        properties_dict = cls.get_base_property_dict_by_character_id(character_id=character_id)
        used_points = 0
        for key in properties_dict:
            used_points += properties_dict[key]
        return used_points

    @classmethod
    def get_additional_property_dict_by_base_property(cls,
                                                      *,
                                                      base_property_type: int,
                                                      ) -> DefaultDict[int, int]:
        kwargs = locals()
        kwargs['additional_source_type'] = AdditionSourceType.BASE_ADDITIONAL.index,
        property_records = cls.get_all_by_kwargs(kwargs=kwargs)
        property_dict = defaultdict(int)
        for property_record in property_records:
            property_dict[property_record.additional_property_type] = property_record.additional_property_value
        return property_dict

    @classmethod
    def get_properties_by_status_id(cls,
                                    *,
                                    status_id: int,
                                    ) -> List["InitialSkillAchievementEquipmentPotionEtcPropertiesRecord"]:
        properties = cls.get_properties_by(additional_source_type=AdditionSourceType.STATUS.index,
                                           additional_source_id=status_id)
        return properties

    @classmethod
    def get_properties_by_base_property(cls,
                                        *,
                                        base_property_id: int,
                                        ) -> List["InitialSkillAchievementEquipmentPotionEtcPropertiesRecord"]:
        properties = cls.get_properties_by(additional_source_type=AdditionSourceType.BASE_ADDITIONAL.index,
                                           additional_source_id=base_property_id)
        return properties

    @classmethod
    def get_properties_by_achievement_id(cls,
                                         *,
                                         achievement_id: int,
                                         ) -> List["InitialSkillAchievementEquipmentPotionEtcPropertiesRecord"]:
        properties = cls.get_properties_by(additional_source_type=AdditionSourceType.ACHIEVEMENT_TITLE.index,
                                           additional_source_id=achievement_id)
        return properties

    @classmethod
    def get_properties_dict_by_skill_book_id(cls,
                                             *,
                                             skill_book_id: int,
                                             ) -> DefaultDict[int, int]:
        """
        获取基础属性对应的属性。分开写函数，减少错误发生
        :return:
        """
        properties_dict = cls.get_properties_dict_by(
            additional_source_type=AdditionSourceType.SKILL.index,
            additional_source_id=skill_book_id,
        )
        return properties_dict

    @classmethod
    def get_properties_dict_by_equipment_record(cls,
                                                *,
                                                equipment_record_id: int,
                                                ) -> DefaultDict[int, int]:
        """
        获取基础属性对应的属性。分开写函数，减少错误发生
        :return:
        """
        properties_dict = cls.get_properties_dict_by(
            additional_source_type=AdditionSourceType.EQUIPMENT_RECORD.index,
            additional_source_id=equipment_record_id,
            property_availability=PropertyAvailability.CURRENT,
        )
        return properties_dict

    @classmethod
    def get_properties_dict_by_potion_id(cls,
                                         *,
                                         potion_id: int,
                                         ) -> DefaultDict[int, int]:
        """
        获取基础属性对应的属性。分开写函数，减少错误发生
        :return:
        """
        properties_dict = cls.get_properties_dict_by(
            additional_source_type=AdditionSourceType.POTION.index,
            additional_source_id=potion_id,
        )
        return properties_dict

    # other
    @classmethod
    def add_skill_book_properties(cls,
                                  *,
                                  skill_book_id: int,
                                  property_index: int,
                                  property_target: int,
                                  property_type: int,
                                  property_value: int
                                  ) -> "InitialSkillAchievementEquipmentPotionEtcPropertiesRecord":
        """
        新增skill book对应的一条属性
        :param skill_book_id: 技能书的id
        :param property_index: 技能的索引
        :param property_target: 属性的作用对象
        :param property_type: 属性的类型
        :param property_value: 属性的值
        :return:
        :rtype:
        """

        property_record = cls.add(additional_source_type=AdditionSourceType.SKILL_BOOK.index,

                                  additional_source_id=skill_book_id,
                                  additional_source_property_index=property_index,
                                  property_availability=property_target,
                                  additional_property_type=property_type,
                                  additional_property_value=property_value,
                                  )
        return property_record

    @classmethod
    def add_status_properties(cls,
                              *,
                              status_id: int,
                              property_index: int,
                              property_type: int,
                              property_value: int) -> "InitialSkillAchievementEquipmentPotionEtcPropertiesRecord":
        property_record = cls.add(additional_source_type=AdditionSourceType.STATUS,
                                  additional_source_id=status_id,
                                  additional_source_property_index=property_index,

                                  additional_property_type=property_type,
                                  additional_property_value=property_value)
        return property_record
