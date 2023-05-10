from collections import defaultdict
import json
import os.path as osp
from typing import List, DefaultDict

import common
from Enums import AdditionSourceType, PartType, EquipmentQuality, AdditionalPropertyType, BeingType, \
    PropertyAvailability, StuffType, part_cn_type_dict, equipment_cn_quality_dict, \
    stuff_cn_type_dict
from DBHelper.db import *
from DBHelper.session import session
import local_setting
from Utils import tools

if __name__ == '__main__':
    equipment_json_src = osp.join(local_setting.json_data_root, "equipment", 'equipment.json')
    equipment_dict_list = tools.file2dict_list(src=equipment_json_src)
    for equipment_dict in equipment_dict_list:
        # 从中文到数字的解析
        part = part_cn_type_dict[equipment_dict['部位']]
        quality = equipment_cn_quality_dict[equipment_dict['品质']]

        # 新增或者更新一个记录；
        equipment_prototype = equipment.add_or_update(name=equipment_dict['名称'],
                                                      part=part,
                                                      quality=quality,
                                                      can_be_identified=equipment_dict['是否可鉴定'],
                                                      introduction=equipment_dict['介绍'],
                                                      is_bind=equipment_dict['是否绑定'],
                                                      )

        # 删除原型装备对应的属性，然后再新建；
        additional_properties_dict = equipment_dict['属性字典']
        misc_properties.del_equipment_prototype_properties(equipment_id=equipment_prototype.id)
        for property_index_str in additional_properties_dict:
            # 解析属性值
            property_index = int(property_index_str)
            prototype_property_items = additional_properties_dict[property_index_str]
            for prototype_property_dict in prototype_property_items:
                property_type = AdditionalPropertyType.name_index_dict[prototype_property_dict['属性类型']]
                misc_properties.add_equipment_properties(
                    additional_property_type=property_type,
                    additional_property_value=prototype_property_dict['最小值'],
                    property_index=property_index,
                    property_availability=PropertyAvailability.MIN,
                )
                misc_properties.add_equipment_properties(
                    additional_property_type=property_type,
                    additional_property_value=prototype_property_dict['最大值'],
                    property_index=property_index,
                    property_availability=PropertyAvailability.MAX,
                )

        # 增加装备对应的分解获得物品的列表，先进行删除；
        open_decompose_or_drop_stuffs.delete_equipment_decompose_get_stuffs(equipment_id=equipment_prototype.id)
        if "分解获得物品列表" in equipment_dict:
            decompose_get_stuff_dict_list = equipment_dict['分解获得物品列表']
            for stuff_dict in decompose_get_stuff_dict_list:
                stuff_type_cn = stuff_dict["物品类型"]
                stuff_type = stuff_cn_type_dict[stuff_type_cn]
                stuff_name = stuff_dict["物品名称"]
                stuff_id = common.get_stuff_id_by_stuff_type_and_name(stuff_type=stuff_type, stuff_name=stuff_name)
