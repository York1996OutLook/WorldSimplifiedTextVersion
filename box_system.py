import os.path as osp
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from typing import List

from DBHelper.db import *
from DBHelper.session import session
from DBHelper.tables.base_table import CustomColumn

from Enums import StuffType
import local_setting
from Utils import tools

Base = declarative_base()


# other
def add_gem_box(*, verbose: bool = False):
    gem_box_json_src = osp.join(local_setting.json_data_root, 'box/gem_box.json')
    gem_box_dict_list = tools.file2dict_list(src=gem_box_json_src)
    for gem_box_dict in gem_box_dict_list:
        # base
        name = gem_box_dict['名字']
        is_bind = gem_box_dict['是否绑定']
        introduction = gem_box_dict['介绍']

        one_box = box.add_or_update_by_name(name=name, is_bind=is_bind, introduction=introduction)

        # 删除源物品对应分解列表，方便后续插入新的值；
        open_decompose_or_drop_stuffs.delete_box_records_by_box_id(box_id=one_box.id)
        if verbose:
            print(f'删除打开{name}对应的物品列表。\n')

        # 插入分解列表
        open_stuffs_dict = gem_box_dict['打开获得物品列表']
        for stuff_dict in open_stuffs_dict:
            stuff_name = stuff_dict["物品名字"]
            stuff_id = gem.get_by_name(name=stuff_name).id
            prob = stuff_dict['概率']
            open_decompose_or_drop_stuffs.add_gem_box(box_id=one_box.id, gem_id=stuff_id, prob=prob)
            if verbose:
                print(f"新增{stuff_name}，概率为{prob}。")


if __name__ == '__main__':
    add_gem_box(verbose=True)
