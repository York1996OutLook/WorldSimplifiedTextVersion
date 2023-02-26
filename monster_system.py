import os.path as osp

import common
from DBHelper.session import session
from DBHelper.db import *
from Enums import DateType, AdditionalPropertyType, date_cn_type_dict, property_cn_type_dict, stuff_cn_type_dict, \
    StuffType
import local_setting
from Utils import tools

if __name__ == '__main__':
    monster_json_src = osp.join(local_setting.json_data_root, "monster", 'monster.json')
    monster_dict_list = tools.file2dict_list(src=monster_json_src)
    for monster_dict in monster_dict_list:
        # base
        name = monster_dict['名称']
        exp_value = monster_dict['经验']
        introduction = monster_dict['描述']
        one_monster = monster.add_or_update(name=name, exp_value=exp_value, introduction=introduction)

        # shows up
        # 删除相关出现的记录，方便后续更新
        monster_show_up_record.del_all_by_monster_id(monster_id=one_monster.id)

        shows_up_date_type = date_cn_type_dict[monster_dict['日期类型']]
        show_up_data_values = monster_dict['具体时间']

        # 添加具体的值；
        for show_up_data_value in show_up_data_values:
            monster_show_up_record.add(monster_id=one_monster.id,
                                       date_type=shows_up_date_type,
                                       date_value=show_up_data_value)

        # 添加对应属性：先删除所有属性
        misc_properties.del_monster_prototype_properties(monster_id=one_monster.id)
        property_dict = monster_dict['属性']
        for property_name in property_dict:
            property_type = property_cn_type_dict[property_name]
            value = property_dict[property_name]
            misc_properties.add_monster_properties(additional_property_type=property_type,
                                                   additional_property_value=value)
        # 添加对应技能，先删除怪物对应技能列表
        player_or_monster_skill_setting.del_monster_skill_setting(monster_id=one_monster.id)
        skill_list = monster_dict["技能设置"]
        for skill_dict in skill_list:
            skill_name = skill_dict['技能名字']
            if skill_name == "":
                continue
            skill_level = skill_dict['技能等级']
            skill_round = skill_dict['释放回合数']

            one_skill = skill.get_skill_by_name(name=skill_name)
            one_skill_book = skill_book.get_by_skill_id_skill_level(skill_id=one_skill.id, level=skill_level)

            player_or_monster_skill_setting.add_monster_skill_setting(monster_id=one_monster.id,
                                                                      skill_book_id=one_skill_book.id)

        # 添加掉落物品的列表和概率；
        drop_stuffs_list = monster_dict['掉落物品']
        drop_n_choose_one_list = []
        for drop_stuff_dict in drop_stuffs_list:
            stuff_type_cn = drop_stuff_dict["物品类型"]
            if stuff_type_cn == "":
                continue
            stuff_level = drop_stuff_dict["等级"]  # 像技能书这样的，会存在等级；
            stuff_type = stuff_cn_type_dict[stuff_type_cn]

            stuff_name = drop_stuff_dict['物品名字']
            stuff_id = common.get_stuff_id_by_stuff_type_and_name(stuff_type=stuff_type,
                                                                  stuff_name=stuff_name,
                                                                  stuff_level=stuff_level)

            prob = drop_stuff_dict['概率']
            open_decompose_or_drop_stuffs.add_monster_drop_equipment(
                monster_id=one_monster.id,
                drop_stuff_type=stuff_type,
                drop_stuff_id=stuff_id,
                drop_stuff_prob=prob,
            )
