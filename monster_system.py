import os.path as osp

from DBHelper.session import session
from DBHelper.db import *
from Enums import DateType, AdditionalPropertyType,date_cn_type_dict
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

        # 添加对应属性：
        attack_speed = monster_dict['出手速度']
        misc_properties
