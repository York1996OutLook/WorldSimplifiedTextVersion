from DBHelper.session import session
from Enums import DateType, AdditionalPropertyType


def add_new_monster_and_etc():
    monster_relevant_dict = {
        # monster base information
        "name": "",
        "exp_value": 100,
        'description': "",
        # When will monster appear
        'date_type': DateType.HOUR_OF_DAY,
        'date_value': 1,
        # battle properties
        AdditionalPropertyType.ATTACK_SPEED: 0,
        AdditionalPropertyType.ATTACK: 0,

        AdditionalPropertyType.HEALTH: 0,
        AdditionalPropertyType.HEALTH_RECOVERY: 0,
        AdditionalPropertyType.HEALTH_ABSORPTION: 0,

        AdditionalPropertyType.MANA: 0,
        AdditionalPropertyType.MANA_RECOVERY: 0,
        AdditionalPropertyType.MANA_ABSORPTION: 0,

        AdditionalPropertyType.COUNTERATTACK: 0,
        AdditionalPropertyType.IGNORE_COUNTERATTACK: 0,

        AdditionalPropertyType.DAMAGE_SHIELD: 0,

        # about skill setting
        "skill_list": [
            {
                'skill_name': None,  # 根据名字查找对应的skill
                'effect_expression': None,
            },
        ],

        "skill_round_skill_dict": {
        }
        # about drop stuffs

    }


if __name__ == '__main__':
    # insert records into Monster table
    monsters = [Monster(name='人形木桩',
                        exp_value=200,
                        description='Ezra曾经是一位荣耀的药剂术士，但是在他对炼药术的不断探索中，他逐渐堕落成了一个邪恶的人物。他开始使用黑暗魔法和危险的材料制作出了许多有害的药剂，并用它们来控制城市中的人们。'),

                Monster(name='药剂术师',
                        exp_value=200,
                        description='Ezra曾经是一位荣耀的药剂术士，但是在他对炼药术的不断探索中，他逐渐堕落成了一个邪恶的人物。他开始使用黑暗魔法和危险的材料制作出了许多有害的药剂，并用它们来控制城市中的人们。'),

                Monster(name='食人魔',
                        exp_value=100,
                        description='一种行动迅速，残忍无情的生物，喜欢吃掉无助的旅行者。'),

                Monster(name='龙', exp_value=450,
                        description='一种以智慧和力量著称的生物，生活在高山和岩石间。')]

    session.add_all([monster1, monster2, monster3])
    session.commit()
