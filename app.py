import time

import battle_property_system
import monster_system
from DBHelper.db import *

import battle_system
from Enums import BeingType, AdditionalPropertyType, AdditionSourceType
import log_system
from Utils import tools


class App:
    def __init__(self, *, player_id: int, nick_name: str):
        """

        :param player_id: qq号，非系统自动生成的id
        :param nick_name: 昵称
        """
        super(App, self).__init__()
        self.player_id = player_id
        self.nick_name = nick_name

    def start(self):
        while True:
            player_input = input("请输入您要执行的操作")
            self.handle_player_input(player_input=player_input)

    def handle_player_input(self, *, player_input: str):
        if player_input == '登陆':
            self.handle_player_log_in_game()
        elif player_input == '属性':
            self.handle_player_query_self_property(player_id=self.player_id)
        elif player_input == "未分配属性点":
            self.handle_player_get_unsigned_point()
        elif player_input == "当前怪物":
            self.handle_player_get_cur_visible_monsters()
        elif player_input[:2] == "挑战":
            self.handle_player_attack_monster(monster_name=player_input[2:])
        elif player_input[:2] in set(base_property_cn_type_dict.keys()):

            # 基础属性名称
            property_type = base_property_cn_type_dict[player_input[:2]]
            std_format = f"{property_type}+1 或者 {property_type}+1"
            # 判断是加还是-属性。后期准备如果-属性，需要扣除对应的黄金
            if len(player_input) < 3:
                print(f"您输入的长度是{len(player_input)},正确的格式是{std_format}。")
                return
            operator = player_input[2]
            if operator == "+":
                is_plus = True
            elif operator == '-':
                is_plus = False
            else:
                print(f'第三个字符请输入+或-，您输入的是{operator}。正确的格式是{std_format}。')
                return

            s = player_input[3:]
            if not tools.is_non_negative_integer(s=s):
                raise ValueError()

            points_num = int(s)
            if points_num == 0:
                print(f"您分配的点数是{points_num},没有意义。正确的格式是{std_format}。")
                return

            self.handle_player_add_or_minus_base_point(property_type=property_type, is_plus=is_plus,
                                                       change_point_num=points_num)
            self.print_cur_base_property_points()

    def handle_player_attack_monster(self, *, monster_name: str):
        if len(monster_name) == 0:
            print('您输入的格式不正确，应该是挑战怪物名字。比如挑战人形木桩')
            return

        one_player = player.get_by_player_id(player_id=self.player_id)

        monster_ids = monster_show_up_record.get_all_monster_id_by_today()

        cur_monster_names = set()
        for monster_id in monster_ids:
            one_monster = monster.get_by_id(_id=monster_id)
            cur_monster_names.add(one_monster.name)

        if monster_name not in cur_monster_names:
            if not monster.is_exists_by_name(name=monster_name):
                print('您要挑战的怪物不存在，请检查您的输入！')
            else:
                print('您要挑战的怪物没有出没，无法进行挑战！')
            return

        one_monster = monster.get_by_name(name=monster_name)

        properties_dict = misc_properties.get_property_dict_by_monster_id(monster_id=one_monster.id)
        properties_intro = "\n".join([f"{property_type_cn_dict[property_type]}:{properties_dict[property_type]}" for
                                      property_type in properties_dict])

        print(f"""您要挑战的怪物是{one_monster.name}，调整成功可以获得经验值{one_monster.exp_value}。
它的相关介绍是:{one_monster.introduction}
相关属性值：{properties_intro}\n""")

        player_properties = battle_property_system.get_player_battle_properties_dict(
            character_id=one_player.id, )

        is_win, battle_log = battle_system.battle(
            positive_name=one_player.nickname,
            positive_battle_properties_dict=player_properties,
            passive_name=one_monster.name,
            passive_battle_properties_dict=properties_dict)

        if is_win:
            monster_system.get_monster_drop_stuffs_by_id(monster_id=one_monster.id)
        print(is_win, battle_log)
        print(1)

    @staticmethod
    def handle_player_get_cur_visible_monsters():
        monster_ids = monster_show_up_record.get_all_monster_id_by_today()
        if len(monster_ids) == 0:
            print("今日没有怪物出现！")
            return
        # todo: 对怪物进行排序
        for idx, monster_id in enumerate(monster_ids):
            one_monster = monster.get_by_id(_id=monster_id)
            print(f'【{idx + 1}】:{one_monster.name}\n经验值：{one_monster.exp_value}\n介绍：{one_monster.introduction}')

    def print_cur_base_property_points(self):
        cur_player = player.get_by_player_id(player_id=self.player_id)
        # 获取已经使用了多少点数
        used_points = misc_properties.get_used_base_property_points_num_by_character_id(character_id=cur_player.id)
        # 根据玩家等级，获取当前一共可以分配多少点数。
        total_points = cur_player.current_level * setting.get_per_level_base_point_num()
        base_properties_dict = misc_properties.get_base_property_dict_by_character_id(character_id=cur_player.id)

        points_signed_string = "\n".join([f"{key} +{base_properties_dict[base_property_cn_type_dict[key]]}" for key in
                                          base_property_cn_type_dict])
        print(f'您当前的属性点分配是:\n\n{points_signed_string}\n\n未分配点数: {total_points - used_points}')

    def handle_player_add_or_minus_base_point(self,
                                              *,
                                              property_type: AdditionalPropertyType,
                                              is_plus: bool,
                                              change_point_num: int):
        cur_player = player.get_by_player_id(player_id=self.player_id)

        # 获取已经使用了多少点数
        used_points = misc_properties.get_used_base_property_points_num_by_character_id(character_id=cur_player.id)
        # 根据玩家等级，获取当前一共可以分配多少点数。
        total_points = cur_player.current_level * setting.get_per_level_base_point_num()
        base_properties_dict = misc_properties.get_base_property_dict_by_character_id(character_id=cur_player.id)
        cur_value = base_properties_dict[property_type]

        if is_plus:
            # 无可分配点数可用
            if total_points - used_points == 0:
                print(f"无可分配点数可用")
                return
            elif used_points + change_point_num > total_points:
                print(f"剩余点数不够，您最多加点{total_points - used_points}")
                return
        else:
            # is minus
            if change_point_num > cur_value:
                print(f'当前{property_type_cn_dict[property_type]}+{cur_value},无法 - {change_point_num}')
                return
            change_point_num = -change_point_num

        # 更新或者新插入加点
        misc_properties.update_or_add_new_base_property(character_id=cur_player.id,
                                                        base_property_type=property_type,
                                                        base_property_value=cur_value + change_point_num)

    def handle_player_get_unsigned_point(self):
        self.print_cur_base_property_points()

    @staticmethod
    def handle_player_query_self_property(*, player_id: int):
        """
        根据player_id id查询角色属性；
        :param player_id:
        :return:
        """
        cur_player = player.get_by_player_id(player_id=player_id)
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
        if not player.is_exists_by_player_id(player_id=self.player_id):
            # 完成新建玩家和玩家对应属性表

            # 新增玩家
            new_player = player.add(player_id=self.player_id,
                                    nickname=self.nick_name,
                                    current_level=setting.get_initial_player_level(),
                                    game_sign=setting.get_player_default_game_sign())
            # 新增玩家对应属性表
            battle_property_system.add_new_player_additional_property_record(character_id=new_player.id)

            # 给新玩家一个初入世界的成就
            one_achievement = achievement.get_by_achievement_name(name='初入世界')
            # 添加到用户的成就记录表中
            player_achievement_record.add(achievement_id=one_achievement.id,
                                          character_id=new_player.id,
                                          achieve_timestamp=int(time.time()))
            # 用户佩戴这个成就称号；
            player.update_achievement_id(character_id=new_player.id, achievement_id=one_achievement.id)

            # 给了新的成就之后要更新玩家的属性
            properties_dict = battle_property_system.get_player_initial_skills_achievements_equipments_properties_dict(
                character_id=new_player.id)
            log_system.log_properties(additional_source_type=AdditionSourceType.PLAYER, properties_dict=properties_dict)
            misc_properties.update_player_properties_dict(character_id=new_player.id, properties_dict=properties_dict)
            print("欢迎进入世界！")
            return
        else:
            print(f"欢迎{self.nick_name}回到游戏！")


if __name__ == '__main__':
    app = App(player_id=603997262, nick_name="York")
    app.start()
