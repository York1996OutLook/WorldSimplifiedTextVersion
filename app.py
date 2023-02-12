import time

import battle_property_system
from DBHelper.tables.player import add_player, is_player_exists_by_player_id
import DBHelper.tables.player_monster_additional_property_record as player_monster_additional_property_record
from DBHelper.tables.player_achievement_record import add_player_achievement_record

import DBHelper.tables.setting as setting
from Enums import BeingType


class App:
    def __init__(self, *, player_id: int, nick_name: str):
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

    def handle_player_log_in_game(self):
        """
        处理玩家进入游戏的函数
        :return:
        """
        if not is_player_exists_by_player_id(player_id=self.player_id):
            # 完成新建玩家和玩家对应属性表

            # 新增玩家
            player = add_player(player_id=self.player_id,
                                nickname=self.nick_name,
                                current_level=setting.get_initial_player_level(),
                                game_sign=setting.get_player_default_game_sign())
            # 新增玩家对应属性表
            record = battle_property_system.add_new_player_additional_property_record(character_id=player.id)
            # 给新玩家一个新人成就
            add_player_achievement_record(achievement_id=1, character_id=player.id, achieve_timestamp=int(time.time()))

            # 给了新的成就之后要更新玩家的属性
            properties_dict = battle_property_system.get_player_initial_skills_achievements_equipments_properties_dict(
                character_id=player.id)
            player_monster_additional_property_record.update_player_monster_additional_properties_record_by_being_and_properties_dict(
                being_type=BeingType.PLAYER,
                being_id=record.being_id,
                properties_dict=properties_dict,
            )
            print("欢迎进入世界！")
            return
        else:
            print(f"欢迎{self.nick_name}回到游戏！")


if __name__ == '__main__':
    app = App(player_id=603997262, nick_name="York")
    app.start()
