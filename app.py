import time

import battle_property_system
from DBHelper.db import *

from Enums import BeingType, property_type_cn_dict, property_cn_type_dict, AdditionalPropertyType, \
    base_property_cn_type_dict
from Utils import tools


class App:
    def __init__(self, *, player_id: int, nick_name: str):
        super(App, self).__init__()
        self.player_id = player_id
        self.nick_name = nick_name
        self.character_id = None

    def start(self):
        while True:
            player_input = input("请输入您要执行的操作")
            self.handle_player_input(player_input=player_input)

    def handle_player_input(self, *, player_input: str):
        if player_input == '登陆':
            self.handle_player_log_in_game()
        elif player_input == '属性':
            self.handle_player_query_self_property(player_id=self.player_id)
        elif player_input == "未分配点数":
            self.handle_player_get_unsigned_point()
        elif player_input[:2] in set(base_property_cn_type_dict.keys()) and player_input[2] in {"+", "-"}:
            property_type = base_property_cn_type_dict[player_input[:2]]
            if player_input[2] == "+":
                is_plus = True
            elif player_input[2] == '-':
                is_plus = False
            else:
                raise ValueError()

            s = player_input[3:]
            if not tools.is_non_negative_integer(s=s):
                raise ValueError()

            points_num = int(s)
            self.handle_player_add_or_minus_base_point(property_type=property_type, is_plus=is_plus,
                                                       change_point_num=points_num)

    def handle_player_add_or_minus_base_point(self,
                                              *,
                                              property_type: AdditionalPropertyType,
                                              is_plus: bool,
                                              change_point_num: int):
        cur_player = player.get_player_by_player_id(player_id=self.player_id)

        used_points = misc_properties.get_used_base_property_points_num(character_id=cur_player.id)
        total_points = cur_player.current_level * setting.get_per_level_base_point_num()
        base_properties_dict = misc_properties.get_base_property_dict_by(character_id=cur_player.id)

        if is_plus:
            if used_points + change_point_num > total_points:
                print(f"剩余点数不够，您最多加点{total_points - used_points}")
                return

        # is minus
        cur_value = base_properties_dict[property_type]
        if change_point_num > cur_value:
            print(f'当前{property_type_cn_dict[property_type]}+{cur_value},无法 - {change_point_num}')
            return
        if not is_plus:
            change_point_num = -change_point_num

        # 更新或者新插入加点
        misc_properties.update_or_add_new_base_property(character_id=cur_player.id,
                                                        base_property_type=property_type,
                                                        base_property_value=
                                                        base_properties_dict[property_type] + change_point_num)

        # 输出当前加点信息
        used_points = misc_properties.get_used_base_property_points_num(character_id=cur_player.id)
        total_points = cur_player.current_level * setting.get_per_level_base_point_num()

        base_properties_dict = misc_properties.get_base_property_dict_by(character_id=cur_player.id)
        points_signed_string = "\n".join([f"{property_type_cn_dict[key]}+{base_properties_dict[key]}" for key in
                                          base_properties_dict])
        print(f'属性点分配成功，你当前的属性点分配是:\n{points_signed_string},未分配点数: {total_points - used_points}')

    def handle_player_get_unsigned_point(self):
        cur_player = player.get_player_by_player_id(player_id=self.player_id)

        level = cur_player.current_level
        all_base_point = setting.get_per_level_base_point_num()
        base_properties_dict = misc_properties.get_base_property_dict_by(character_id=cur_player.id)
        print(1)

    @staticmethod
    def handle_player_query_self_property(*, player_id: int):
        """
        根据player_id id查询角色属性；
        :param player_id:
        :return:
        """
        cur_player = player.get_player_by_player_id(player_id=player_id)
        properties_dict = battle_property_system.get_player_initial_skills_achievements_equipments_properties_dict(
            character_id=cur_player.id)
        for property_type in properties_dict:
            value = properties_dict[property_type]
            if value != 0:
                print(property_type_cn_dict[property_type], value)

    def handle_player_log_in_game(self):
        """
        处理玩家进入游戏的函数
        :return:
        """
        if not player.is_player_exists_by_player_id(player_id=self.player_id):
            # 完成新建玩家和玩家对应属性表

            # 新增玩家
            new_player = player.add_player(player_id=self.player_id,
                                           nickname=self.nick_name,
                                           current_level=setting.get_initial_player_level(),
                                           game_sign=setting.get_player_default_game_sign())
            # 新增玩家对应属性表
            battle_property_system.add_new_player_additional_property_record(character_id=new_player.id)

            # 给新玩家一个初入世界的成就
            one_achievement = achievement.get_achievement_by_achievement_name(name='初入世界')
            # 添加到用户的成就记录表中
            player_achievement_record.add_player_achievement_record(achievement_id=one_achievement.id,
                                                                    character_id=new_player.id,
                                                                    achieve_timestamp=int(time.time()))
            # 用户佩戴这个成就称号；
            player.update_player_achievement_id(character_id=new_player.id, achievement_id=one_achievement.id)

            # 给了新的成就之后要更新玩家的属性
            properties_dict = battle_property_system.get_player_initial_skills_achievements_equipments_properties_dict(
                character_id=new_player.id)

            player_monster_additional_property_record.update_player_monster_additional_properties_record_by_being_and_properties_dict(
                being_type=BeingType.PLAYER,
                being_id=new_player.id,
                properties_dict=properties_dict,
            )
            print("欢迎进入世界！")
            return
        else:
            print(f"欢迎{self.nick_name}回到游戏！")


if __name__ == '__main__':
    app = App(player_id=603997262, nick_name="York")
    app.start()
