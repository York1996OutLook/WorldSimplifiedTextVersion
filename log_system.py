from collections import defaultdict
from typing import List, DefaultDict

from Enums import BattlePropertyType, AdditionSourceType, AdditionalPropertyType, BeingType, \
    PropertyAvailability, addition_source_type_cn_dict, property_type_cn_dict
from DBHelper.db import *

from DBHelper.session import session

import potion_system


def log_properties(*, additional_source_type: AdditionSourceType, properties_dict: DefaultDict[int, int]):
    """
    对属性进行输出，减少代码编写错误
    :param additional_source_type:
    :param properties_dict:
    :return:
    """
    additional_source_type_cn = addition_source_type_cn_dict[additional_source_type]
    print(f"属性来源：{{{additional_source_type_cn}}}")
    for property_type in properties_dict:
        print(f"""
        属性【{property_type_cn_dict[property_type]}】={properties_dict[property_type]}
        """.strip())
