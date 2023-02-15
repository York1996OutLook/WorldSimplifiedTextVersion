from collections import defaultdict
from typing import List, DefaultDict

from Enums import AdditionSourceType, PartType, EquipmentQuality, AdditionalPropertyType, BeingType, \
    EquipmentPropertyAvailability, StuffType
from DBHelper.db import *

from DBHelper.session import session

"""
equipment_list = [
        {
            # base
            'name': "",
            'part': PartType.LEG,
            'quality': EquipmentQuality.COMMON,
            'is_bind': False,
            'can_be_identified': False,
            'introduction': '',
            # properties
            "additional_properties_dict": {
                # 第一条属性
                1:[
                    {
                        "min_property_type": AdditionalPropertyType.MANA,
                        "min_property_value": 1,
                        
                        "max_property_type": AdditionalPropertyType.MANA,
                        "max_property_value": 10,
                    },
                ],
                2:[
                    {
                        "min_property_type": AdditionalPropertyType.MANA,
                        "min_property_value": 1,

                        "max_property_type": AdditionalPropertyType.MANA,
                        "max_property_value": 10,

                    },
                ],
                3: [
                    {
                        "min_property_type": AdditionalPropertyType.MANA,
                        "min_property_value": 1,

                        "max_property_type": AdditionalPropertyType.MANA,
                        "max_property_value": 1,

                    },
                ],
                4: [ 
                    {
                        "min_property_type": AdditionalPropertyType.MANA,
                        "min_property_value": 1,

                        "max_property_type": AdditionalPropertyType.MANA,
                        "max_property_value": 1,

                    },
                ]
            }
        }
    ]

"""


def add_equipment():
    equipment_quality_decompose_stuff_dict = {
        EquipmentQuality.COMMON: {
            [
                # 5*50
                *[{
                    'get_stuff_type': StuffType.IDENTIFY_BOOK,
                    'get_stuff_value': 1,
                    'get_stuff_prob': 50,
                }for _ in range(1)],

                # 5*50
                *[{
                    'get_stuff_type': StuffType.RAISE_STAR_BOOK,
                    'get_stuff_value': 1,
                    'get_stuff_prob': 50,
                } for _ in range(1)],
            ]
        },
        EquipmentQuality.EXCELLENT: {
            [
                # 5*50
                *[{
                    'get_stuff_type': StuffType.IDENTIFY_BOOK,
                    'get_stuff_value': 1,
                    'get_stuff_prob': 50,
                }for _ in range(3)],

                # 5*50
                *[{
                    'get_stuff_type': StuffType.RAISE_STAR_BOOK,
                    'get_stuff_value': 1,
                    'get_stuff_prob': 50,
                } for _ in range(3)],
            ]
        },
        EquipmentQuality.RARE: {
            [
                # 5*50
                *[{
                    'get_stuff_type': StuffType.IDENTIFY_BOOK,
                    'get_stuff_value': 1,
                    'get_stuff_prob': 50,
                }for _ in range(5)],

                # 5*50
                *[{
                    'get_stuff_type': StuffType.RAISE_STAR_BOOK,
                    'get_stuff_value': 1,
                    'get_stuff_prob': 50,
                } for _ in range(5)],
            ]
        },
        EquipmentQuality.EPIC: {
            [
                # 5*50
                *[{
                    'get_stuff_type': StuffType.IDENTIFY_BOOK,
                    'get_stuff_value': 1,
                    'get_stuff_prob': 50,
                }for _ in range(7)],

                # 5*50
                *[{
                    'get_stuff_type': StuffType.RAISE_STAR_BOOK,
                    'get_stuff_value': 1,
                    'get_stuff_prob': 50,
                } for _ in range(7)],
            ]
        },
        EquipmentQuality.MYTHIC: {
            [
                # 5*50
                *[{
                    'get_stuff_type': StuffType.IDENTIFY_BOOK,
                    'get_stuff_value': 1,
                    'get_stuff_prob': 50,
                }for _ in range(9)],

                # 5*50
                *[{
                    'get_stuff_type': StuffType.RAISE_STAR_BOOK,
                    'get_stuff_value': 1,
                    'get_stuff_prob': 50,
                } for _ in range(9)],
            ]
        },
        EquipmentQuality.MYTHOLOGY: {
            [
                # 5*50
                *[{
                    'get_stuff_type': StuffType.IDENTIFY_BOOK,
                    'get_stuff_value': 1,
                    'get_stuff_prob': 50,
                } for _ in range(11)],

                # 5*50
                *[{
                    'get_stuff_type': StuffType.RAISE_STAR_BOOK,
                    'get_stuff_value': 1,
                    'get_stuff_prob': 50,
                } for _ in range(11)],
            ]
        },
    }

    equipment_list = [
        ###################################################################
        {
            # base
            'name': "木制头盔",
            'part': PartType.HEAD,
            'quality': EquipmentQuality.COMMON,
            'is_bind': False,
            "can_be_identified": False,
            'introduction': '木头做的头盔，穿起来感觉很不舒服。',
            # properties
            "additional_properties_dict": {
                # 第一条属性
                1: [
                    {
                        "property_type": AdditionalPropertyType.HEALTH,
                        "min_property_value": 25,
                        "max_property_value": 25,
                    },
                ],
            },
            # 分解获得的装备和概率
            "decompose_get_stuffs": equipment_quality_decompose_stuff_dict[EquipmentQuality.COMMON]
        },
        ########################################################################
        ###################################################################
        {
            # base
            'name': "木制护肩",
            'part': PartType.SHOULDER,
            'quality': EquipmentQuality.COMMON,
            'is_bind': False,
            "can_be_identified": False,
            'introduction': '木头做的护肩，穿起来感觉很不舒服。',
            # properties
            "additional_properties_dict": {
                # 第一条属性
                1: [
                    {
                        "min_property_type": AdditionalPropertyType.HEALTH,
                        "min_property_value": 25,

                        "max_property_type": AdditionalPropertyType.HEALTH,
                        "max_property_value": 25,
                    },
                ],
            },
            # 分解获得的装备和概率
            "decompose_get_stuffs": equipment_quality_decompose_stuff_dict[EquipmentQuality.COMMON]
        },
        ########################################################################
        ###################################################################
        {
            # base
            'name': "木制盔甲",
            'part': PartType.CLOTHES,
            'quality': EquipmentQuality.COMMON,
            'is_bind': False,
            "can_be_identified": False,
            'introduction': '木头做的盔甲，穿起来感觉很不舒服。',
            # properties
            "additional_properties_dict": {
                # 第一条属性
                1: [
                    {
                        "min_property_type": AdditionalPropertyType.HEALTH,
                        "min_property_value": 25,

                        "max_property_type": AdditionalPropertyType.HEALTH,
                        "max_property_value": 25,
                    },
                ],
            },
            # 分解获得的装备和概率
            "decompose_get_stuffs": equipment_quality_decompose_stuff_dict[EquipmentQuality.COMMON]
        },
        ########################################################################
        ###################################################################
        {
            # base
            'name': "木制护腰",
            'part': PartType.WAIST,
            'quality': EquipmentQuality.COMMON,
            'is_bind': False,
            "can_be_identified": False,
            'introduction': '木头做的护腰，穿起来感觉很不舒服。',
            # properties
            "additional_properties_dict": {
                # 第一条属性
                1: [
                    {
                        "min_property_type": AdditionalPropertyType.HEALTH,
                        "min_property_value": 25,

                        "max_property_type": AdditionalPropertyType.HEALTH,
                        "max_property_value": 25,
                    },
                ],
            },
            # 分解获得的装备和概率
            "decompose_get_stuffs": equipment_quality_decompose_stuff_dict[EquipmentQuality.COMMON]
        },
        ########################################################################
        ###################################################################
        {
            # base
            'name': "木制护手",
            'part': PartType.HAND,
            'quality': EquipmentQuality.COMMON,
            'is_bind': False,
            "can_be_identified": False,
            'introduction': '木头做的护手，穿起来感觉很不舒服。',
            # properties
            "additional_properties_dict": {
                # 第一条属性
                1: [
                    {
                        "min_property_type": AdditionalPropertyType.HEALTH,
                        "min_property_value": 25,

                        "max_property_type": AdditionalPropertyType.HEALTH,
                        "max_property_value": 25,
                    },
                ],
            },
            # 分解获得的装备和概率
            "decompose_get_stuffs": equipment_quality_decompose_stuff_dict[EquipmentQuality.COMMON]
        },
        ########################################################################
        ###################################################################
        {
            # base
            'name': "木制护腿",
            'part': PartType.HEAD,
            'quality': EquipmentQuality.COMMON,
            'is_bind': False,
            "can_be_identified": False,
            'introduction': '木头做的护腿，穿起来感觉很不舒服。',
            # properties
            "additional_properties_dict": {
                # 第一条属性
                1: [
                    {
                        "min_property_type": AdditionalPropertyType.HEALTH,
                        "min_property_value": 25,

                        "max_property_type": AdditionalPropertyType.HEALTH,
                        "max_property_value": 25,
                    },
                ],
            },
            # 分解获得的装备和概率
            "decompose_get_stuffs": equipment_quality_decompose_stuff_dict[EquipmentQuality.COMMON]
        },
        ########################################################################
        ###################################################################
        {
            # base
            'name': "木制护足",
            'part': PartType.FOOT,
            'quality': EquipmentQuality.COMMON,
            'is_bind': False,
            "can_be_identified": False,
            'introduction': '木头做的护足，穿起来感觉很不舒服。',
            # properties
            "additional_properties_dict": {
                # 第一条属性
                1: [
                    {
                        "min_property_type": AdditionalPropertyType.HEALTH,
                        "min_property_value": 25,

                        "max_property_type": AdditionalPropertyType.HEALTH,
                        "max_property_value": 25,
                    },
                ],
            },
            # 分解获得的装备和概率
            "decompose_get_stuffs": equipment_quality_decompose_stuff_dict[EquipmentQuality.COMMON]
        },
        ########################################################################
        ###################################################################
        {
            # base
            'name': "木制短剑",
            'part': PartType.WEAPON,
            'quality': EquipmentQuality.COMMON,
            'is_bind': False,
            "can_be_identified": False,
            'introduction': '仅需两块木板和一根木棍，你就能得到一把木制短剑！',
            # properties
            "additional_properties_dict": {
                # 第一条属性
                1: [
                    {
                        "min_property_type": AdditionalPropertyType.ATTACK,
                        "min_property_value": 5,

                        "max_property_type": AdditionalPropertyType.ATTACK,
                        "max_property_value": 5,
                    },
                ],
            },
            # 分解获得的装备和概率
            "decompose_get_stuffs": equipment_quality_decompose_stuff_dict[EquipmentQuality.COMMON]
        },
        ########################################################################
        {
            ###################################################################
            # base
            'name': "木制盾牌",
            'part': PartType.WEAPON,
            'quality': EquipmentQuality.COMMON,
            'is_bind': False,
            'introduction': '木制盾牌是一件充满历史色彩的防御装备，它的设计受到古代战士的启发，在保证防御性能的同时，也体现出了高超的手工技艺。',
            # properties
            "additional_properties_dict": {
                # 第一条属性
                1: [
                    {
                        "min_property_type": AdditionalPropertyType.HEALTH,
                        "min_property_value": 20,

                        "max_property_type": AdditionalPropertyType.HEALTH,
                        "max_property_value": 20,
                    },
                ],
            },
            # 分解获得的装备和概率
            "decompose_get_stuffs": equipment_quality_decompose_stuff_dict[EquipmentQuality.COMMON]
        },
        ########################################################################

        ###################################################################
        {
            # base
            'name': "木马",
            'part': PartType.MOUNT,
            'quality': EquipmentQuality.COMMON,
            'is_bind': False,
            'introduction': '你可以坐上去获得更好的视野，但是好像它并不会移动；',
            # properties
            "additional_properties_dict": {
                # 第一条属性
                1: [
                    {
                        "min_property_type": AdditionalPropertyType.HEALTH_ADD_PERCENT,
                        "min_property_value": 5,

                        "max_property_type": AdditionalPropertyType.HEALTH_ADD_PERCENT,
                        "max_property_value": 5,
                    },
                ],
            },
            "decompose_get_stuffs": equipment_quality_decompose_stuff_dict[EquipmentQuality.COMMON]
        },
        ########################################################################

        ###################################################################
        {
            # base
            'name': "木制项链",
            'part': PartType.NECKLACE,
            'quality': EquipmentQuality.COMMON,
            'is_bind': False,
            'introduction': '你可以坐上去获得更好的视野，但是好像它并不会移动；',
            # properties
            "additional_properties_dict": {
                # 第一条属性
                1: [
                    {
                        "min_property_type": AdditionalPropertyType.PHYSIQUE,
                        "min_property_value": 5,

                        "max_property_type": AdditionalPropertyType.PHYSIQUE,
                        "max_property_value": 5,
                    },
                    {
                        "min_property_type": AdditionalPropertyType.PHYSIQUE,
                        "min_property_value": 5,

                        "max_property_type": AdditionalPropertyType.PHYSIQUE,
                        "max_property_value": 5,
                    },
                    {
                        "min_property_type": AdditionalPropertyType.PHYSIQUE,
                        "min_property_value": 5,

                        "max_property_type": AdditionalPropertyType.PHYSIQUE,
                        "max_property_value": 5,
                    },
                    {
                        "min_property_type": AdditionalPropertyType.PHYSIQUE,
                        "min_property_value": 5,

                        "max_property_type": AdditionalPropertyType.PHYSIQUE,
                        "max_property_value": 5,
                    },
                ],
            },
            "decompose_get_stuffs": equipment_quality_decompose_stuff_dict[EquipmentQuality.COMMON]
        },
        ########################################################################
    ]

    if __name__ == '__main__':
        exp_books = [
            ExpBook(base_property_type=ExpBookType.CHARACTER, exp_value=500),
            ExpBook(base_property_type=ExpBookType.CHARACTER, exp_value=3000),
            ExpBook(base_property_type=ExpBookType.CHARACTER, exp_value=10000),
            ExpBook(base_property_type=ExpBookType.CHARACTER, exp_value=20000),
        ]

        session.add_all(exp_books)
        session.commit()
