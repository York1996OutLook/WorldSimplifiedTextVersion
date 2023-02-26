from typing import DefaultDict

import time
from DBHelper.db import *

from Enums import BeingType, property_type_cn_dict, property_cn_type_dict, AdditionalPropertyType, \
    base_property_cn_type_dict
from Utils import tools


def battle(*, positive_battle_properties_dict: DefaultDict[int, int],
           passive_battle_properties_dict: DefaultDict[int, int], ):
    print(1)
