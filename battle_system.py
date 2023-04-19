from typing import DefaultDict, Tuple
import time

import numpy as np
from DBHelper.db import *

from Enums import BeingType, AdditionalPropertyType
from Utils import tools


class BattleBeing:
    def __init__(self, *, name: str, origin_dict: DefaultDict[int, int], is_positive: bool):
        """

        :param name:名称
        :param origin_dict:初始字典
        :param is_positive:是否为主动攻击的人
        """
        self.name = name
        self.origin_property_dict = origin_dict.copy()
        self.cur_property_dict = origin_dict.copy()
        self.states = set()
        self.is_positive = is_positive


def battle(*,
           positive_name: str,
           positive_battle_properties_dict: DefaultDict[int, int],
           passive_name: str,
           passive_battle_properties_dict: DefaultDict[int, int],
           ) -> Tuple[bool, str]:
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
    # 战斗相关属性设置
    percent100_critical_point = setting.get_percent100_critical_point()
    critical_damage_multiplier = setting.get_critical_damage_multiplier()
    percent100_counterattack = setting.get_percent100_counterattack()
    percent100_health_absorption = setting.get_percent100_health_absorption()
    percent100_mana_absorption = setting.get_percent100_mana_absorption()

    being1 = BattleBeing(name=positive_name, origin_dict=positive_battle_properties_dict, is_positive=True)
    being2 = BattleBeing(name=passive_name, origin_dict=passive_battle_properties_dict, is_positive=False)

    total_round = setting.get_max_battle_round_num()

    battle_log = ""
    for round_index in range(1, total_round + 1):
        battle_log += f"\n第【{round_index}】回合："
        if being1.cur_property_dict[AdditionalPropertyType.ATTACK_SPEED] < being2.cur_property_dict[
            AdditionalPropertyType.ATTACK_SPEED]:
            being1, being2 = being2, being1

        battle_log += f"{being1.name}【出手速度】{being1.cur_property_dict[AdditionalPropertyType.ATTACK_SPEED]}大于{being2.name}的{being2.cur_property_dict[AdditionalPropertyType.ATTACK_SPEED]}，先出手！"
        for p1, p2 in [
            (being1, being2),
            (being2, being1),
        ]:
            attack_damage = p1.cur_property_dict[AdditionalPropertyType.ATTACK]
            critical_prob = p1.cur_property_dict[AdditionalPropertyType.CRITICAL_POINT] / percent100_critical_point
            damage_shield = p2.cur_property_dict[AdditionalPropertyType.DAMAGE_SHIELD]

            if damage_shield > 0:
                being1.cur_property_dict[AdditionalPropertyType.DAMAGE_SHIELD] -= 1
                battle_log = f"{being2.name}消耗一层免伤护盾【{damage_shield}->{damage_shield - 1}】抵消了伤害；"
            else:
                # 没有免伤护盾则需要承受伤害
                # 可能产生暴击伤害；
                if critical_prob >= np.random.random():
                    battle_log += f"暴击！伤害{attack_damage}{critical_damage_multiplier}"
                    attack_damage *= critical_damage_multiplier

                if attack_damage>0:
                    battle_log += f"{p2.name}【生命值】{p2.cur_property_dict[AdditionalPropertyType.HEALTH]}-{attack_damage}={p2.cur_property_dict[AdditionalPropertyType.HEALTH] - attack_damage}。"
                    p2.cur_property_dict[AdditionalPropertyType.HEALTH] -= attack_damage
                    if p2.cur_property_dict[AdditionalPropertyType.HEALTH] <= 0:
                        battle_log += f"战斗结束，{p1.name}取得胜利！"
                        is_win = p1.is_positive
                        return is_win,battle_log

                # p1 生命吸收，法力吸收
                health_absorption = int(attack_damage * p1.cur_property_dict[
                    AdditionalPropertyType.HEALTH_ABSORPTION] / percent100_health_absorption)
                mana_absorption = int(attack_damage * p1.cur_property_dict[
                    AdditionalPropertyType.MANA_ABSORPTION] / percent100_mana_absorption)
                temp_health = p1.cur_property_dict[AdditionalPropertyType.HEALTH] + health_absorption   # 防止超限；
                temp_mana = p1.cur_property_dict[AdditionalPropertyType.MANA] + mana_absorption

                p1.cur_property_dict[AdditionalPropertyType.HEALTH] = min(temp_health,
                                                                          p1.cur_property_dict[AdditionalPropertyType.HEALTH])
                p1.cur_property_dict[AdditionalPropertyType.MANA] = min(temp_mana,
                                                                        p1.cur_property_dict[AdditionalPropertyType.MANA])

                if health_absorption != 0:
                    battle_log += f"{p1.name}吸收生命{health_absorption}，当前生命{p1.cur_property_dict[AdditionalPropertyType.HEALTH]}。"
                if mana_absorption != 0:
                    battle_log += f"{p1.name}吸收法力{mana_absorption}，当前法力{p1.cur_property_dict[AdditionalPropertyType.MANA]}。"

            # 进行反击的过程
            if p1.cur_property_dict[AdditionalPropertyType.IGNORE_COUNTERATTACK] < p2.cur_property_dict[
                AdditionalPropertyType.COUNTERATTACK]:
                counterattack_damage = (p2.cur_property_dict[AdditionalPropertyType.COUNTERATTACK] -
                                        p1.cur_property_dict[AdditionalPropertyType.IGNORE_COUNTERATTACK]) \
                                       / percent100_counterattack * attack_damage
                origin_health = p1.cur_property_dict[AdditionalPropertyType.HEALTH]
                p1.cur_property_dict[AdditionalPropertyType.HEALTH] -= counterattack_damage
                battle_log += f"{p1.name}【生命值】={origin_health}，受到反击伤害为{p1.cur_property_dict[AdditionalPropertyType.COUNTERATTACK] - p1.cur_property_dict[AdditionalPropertyType.IGNORE_COUNTERATTACK]}*{attack_damage}={counterattack_damage}点反击伤害。生命值为{p1.cur_property_dict[AdditionalPropertyType.HEALTH]}"
                if p2.cur_property_dict[AdditionalPropertyType.HEALTH] <= 0:
                    battle_log += f"战斗结束，{p1.name}取得胜利！"
                    is_win = p1.is_positive
                    return is_win,battle_log

        # end of round
        # 回复生命不超过最大生命和法力值
        temp_health = being1.cur_property_dict[AdditionalPropertyType.HEALTH] + being1.cur_property_dict[AdditionalPropertyType.HEALTH_RECOVERY]
        temp_mana = being1.cur_property_dict[AdditionalPropertyType.MANA] + being1.cur_property_dict[AdditionalPropertyType.MANA_RECOVERY]

        being1.cur_property_dict[AdditionalPropertyType.HEALTH] = min(temp_health, being1.origin_property_dict[AdditionalPropertyType.HEALTH])
        being1.cur_property_dict[AdditionalPropertyType.MANA] = min(temp_mana, being1.origin_property_dict[AdditionalPropertyType.MANA])

        if being1.cur_property_dict[AdditionalPropertyType.HEALTH_RECOVERY] != 0:
            battle_log += f"{being1.name}回复生命{being1.cur_property_dict[AdditionalPropertyType.HEALTH_RECOVERY]}，当前【生命】{being1.cur_property_dict[AdditionalPropertyType.HEALTH]}。"
        if being1.cur_property_dict[AdditionalPropertyType.MANA_RECOVERY] != 0:
            battle_log += f"{being1.name}回复法力{being1.cur_property_dict[AdditionalPropertyType.HEALTH_RECOVERY]}，当前【法力】{being1.cur_property_dict[AdditionalPropertyType.MANA]}。"

        temp_health = being2.cur_property_dict[AdditionalPropertyType.HEALTH] + being2.cur_property_dict[AdditionalPropertyType.HEALTH_RECOVERY]
        temp_mana = being2.cur_property_dict[AdditionalPropertyType.MANA] + being2.cur_property_dict[AdditionalPropertyType.MANA_RECOVERY]

        being2.cur_property_dict[AdditionalPropertyType.HEALTH] = min(temp_health, being2.origin_property_dict[AdditionalPropertyType.HEALTH])
        being2.cur_property_dict[AdditionalPropertyType.MANA] = min(temp_mana, being2.origin_property_dict[AdditionalPropertyType.MANA])

        if being2.cur_property_dict[AdditionalPropertyType.HEALTH_RECOVERY] != 0:
            battle_log += f"{being2.name}回复生命{being2.cur_property_dict[AdditionalPropertyType.HEALTH_RECOVERY]}，当前生命{being2.cur_property_dict[AdditionalPropertyType.HEALTH]}"
        if being2.cur_property_dict[AdditionalPropertyType.MANA_RECOVERY] != 0:
            battle_log += f"{being2.name}回复法力{being2.cur_property_dict[AdditionalPropertyType.MANA_RECOVERY]}，当前法力{being2.cur_property_dict[AdditionalPropertyType.MANA]}"

    # 回合结束没有决出胜负，则主动攻击者算作失败！
    battle_log += "战斗结束，超过最大回合数，挑战失败！"
    return False, battle_log
