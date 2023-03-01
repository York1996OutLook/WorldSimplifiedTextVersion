from typing import DefaultDict
import time

import numpy as np
from DBHelper.db import *

from Enums import BeingType, property_type_cn_dict, property_cn_type_dict, AdditionalPropertyType, \
    base_property_cn_type_dict
from Utils import tools


def battle(*,
           positive_name: str,
           positive_battle_properties_dict: DefaultDict[int, int],
           passive_name: str,
           passive_battle_properties_dict: DefaultDict[int, int], ):
    """
    实现两个玩家对战，将对战的详细过程记录在battle_log中。涉及战斗的属性有：
    出手速度（决定了谁先出手），
    攻击力（决定了对方收到的伤害），

    致命点（决定了产生暴击的概率，暴击伤害将会使得真实伤害翻倍），

    生命值（决定了最多可以承受多少伤害），
    生命值回复（决定了回合结束之后，会回复多少生命值），
    生命值吸收（对对手造成伤害之后，会按照百分比回复自己的生命），

    免伤护盾（决定了可以抵消的伤害次数），

    反击值（决定了可以反击对对手自己受到伤害的百分比），
    无视反击值（决定了可以无视对手的多少反击值），

    :param positive_battle_properties_dict:
    :param passive_battle_properties_dict:
    :param positive_name:
    :param passive_name:
    :return:
    """
    percent100_critical_point = setting.get_percent100_critical_point()
    critical_damage_multiplier = setting.get_critical_damage_multiplier()
    percent100_counterattack = setting.get_percent100_counterattack()
    percent100_health_absorption = setting.get_percent100_health_absorption()
    percent100_mana_absorption = setting.get_percent100_mana_absorption()

    being1_dict = positive_battle_properties_dict.copy()
    being2_dict = passive_battle_properties_dict.copy()

    total_round = setting.get_max_battle_round_num()

    battle_log = ""
    for round_index in range(1, total_round + 1):
        battle_log += f"第【{round_index}】回合："
        if being1_dict[AdditionalPropertyType.ATTACK_SPEED] > being2_dict[AdditionalPropertyType.ATTACK_SPEED]:
            player1_origin_dict = positive_battle_properties_dict.copy()
            player2_origin_dict = passive_battle_properties_dict.copy()

            player1_dict = being1_dict
            player1_name = positive_name

            player2_dict = being2_dict
            player2_name = passive_name
        else:
            player1_origin_dict = passive_battle_properties_dict.copy()
            player2_origin_dict = positive_battle_properties_dict.copy()
            player1_dict = being2_dict
            player1_name = passive_name

            player2_dict = being1_dict
            player2_name = positive_name

        for p1_name, p1_dict, p1_origin_dict, p2_name, p2_dict, p2_origin_dict in [
            (player1_name, player1_dict, player1_origin_dict, player2_name, player2_dict, player2_origin_dict),
            (player2_name, player2_dict, player2_origin_dict, player1_name, player1_dict, player1_origin_dict),
        ]:
            battle_log += f"{p1_name}【出手速度】{being1_dict[AdditionalPropertyType.ATTACK_SPEED]}大于{p2_name}的{being2_dict[AdditionalPropertyType.ATTACK_SPEED]}，先出手！"

            attack_damage = p1_dict[AdditionalPropertyType.ATTACK]
            critical_prob = p1_dict[AdditionalPropertyType.CRITICAL_POINT] / percent100_critical_point
            damage_shield = p2_dict[AdditionalPropertyType.DAMAGE_SHIELD]

            if damage_shield > 0:
                damage_shield -= 1
                battle_log = f"{p2_name}消耗一层免伤护盾抵消了伤害；"
            else:
                # 没有免伤护盾则需要承受伤害
                # 可能产生暴击伤害；
                if critical_prob >= np.random.random():
                    battle_log += f"暴击！伤害{attack_damage}{critical_damage_multiplier}"
                    attack_damage *= critical_damage_multiplier

                battle_log += f"{p2_name}【生命值】{p2_dict[AdditionalPropertyType.HEALTH]}-{attack_damage}={p2_dict[AdditionalPropertyType.HEALTH] - attack_damage}。"
                p2_dict[AdditionalPropertyType.HEALTH] -= attack_damage
                if p2_dict[AdditionalPropertyType.HEALTH] <= 0:
                    battle_log += f"战斗结束，{p2_name}取得胜利！"
                    return battle_log

                # p1 生命吸收，法力吸收
                health_absorption = int(attack_damage * p1_dict[
                    AdditionalPropertyType.HEALTH_ABSORPTION] / percent100_health_absorption)
                mana_absorption = int(attack_damage * p1_dict[
                    AdditionalPropertyType.MANA_ABSORPTION] / percent100_mana_absorption)
                temp_health = p1_dict[AdditionalPropertyType.HEALTH] + health_absorption
                temp_mana = p1_dict[AdditionalPropertyType.MANA] + mana_absorption

                p1_dict[AdditionalPropertyType.HEALTH] = min(temp_health,
                                                             p1_origin_dict[AdditionalPropertyType.HEALTH])
                p1_dict[AdditionalPropertyType.MANA] = min(temp_mana, p1_origin_dict[AdditionalPropertyType.MANA])

                battle_log += f"{p1_name}吸收生命{health_absorption}，当前生命{p1_dict[AdditionalPropertyType.HEALTH]}"
                battle_log += f"{p1_name}吸收法力{health_absorption}，当前法力{p1_dict[AdditionalPropertyType.MANA]}"

            # 进行反击的过程
            if p1_dict[AdditionalPropertyType.IGNORE_COUNTERATTACK] < p2_dict[AdditionalPropertyType.COUNTERATTACK]:
                counterattack_damage = (p2_dict[AdditionalPropertyType.COUNTERATTACK] -
                                        p1_dict[AdditionalPropertyType.IGNORE_COUNTERATTACK]) \
                                       / percent100_counterattack * attack_damage
                origin_health = p1_dict[AdditionalPropertyType.HEALTH]
                p1_dict[AdditionalPropertyType.HEALTH] -= counterattack_damage
                battle_log += f"{p1_name}【生命值】={origin_health}，受到反击伤害为{p1_dict[AdditionalPropertyType.COUNTERATTACK] - p1_dict[AdditionalPropertyType.IGNORE_COUNTERATTACK]}*{attack_damage}={counterattack_damage}点反击伤害。生命值为{p1_dict[AdditionalPropertyType.HEALTH]}"
                if p2_dict[AdditionalPropertyType.HEALTH] <= 0:
                    battle_log += f"战斗结束，{p2_name}取得胜利！"
                    return battle_log

            # end of round
            # 回复生命不超过最大生命和法力值
            temp_health = p1_dict[AdditionalPropertyType.HEALTH] + p1_dict[AdditionalPropertyType.HEALTH_RECOVERY]
            temp_mana = p1_dict[AdditionalPropertyType.HEALTH] + p1_dict[AdditionalPropertyType.HEALTH_RECOVERY]

            p1_dict[AdditionalPropertyType.HEALTH] = min(temp_health, p1_origin_dict[AdditionalPropertyType.HEALTH])
            p1_dict[AdditionalPropertyType.MANA] = min(temp_mana, p1_origin_dict[AdditionalPropertyType.MANA])

            battle_log += f"{p1_name}回复生命{p1_dict[AdditionalPropertyType.HEALTH_RECOVERY]}，当前生命{p1_dict[AdditionalPropertyType.HEALTH]}"
            battle_log += f"{p1_name}回复法力{p1_dict[AdditionalPropertyType.HEALTH_RECOVERY]}，当前法力{p1_dict[AdditionalPropertyType.MANA]}"

            temp_health = p2_dict[AdditionalPropertyType.HEALTH] + p2_dict[AdditionalPropertyType.HEALTH_RECOVERY]
            temp_mana = p2_dict[AdditionalPropertyType.HEALTH] + p2_dict[AdditionalPropertyType.HEALTH_RECOVERY]

            p2_dict[AdditionalPropertyType.HEALTH] = min(temp_health, p2_origin_dict[AdditionalPropertyType.HEALTH])
            p2_dict[AdditionalPropertyType.MANA] = min(temp_mana, p2_origin_dict[AdditionalPropertyType.MANA])

            battle_log += f"{p2_name}回复生命{p2_dict[AdditionalPropertyType.HEALTH_RECOVERY]}，当前生命{p2_dict[AdditionalPropertyType.HEALTH]}"
            battle_log += f"{p2_name}回复法力{p2_dict[AdditionalPropertyType.HEALTH_RECOVERY]}，当前法力{p2_dict[AdditionalPropertyType.MANA]}"
