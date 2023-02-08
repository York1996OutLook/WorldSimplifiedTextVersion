import time
from DBHelper.tables.player import Player, add_player, is_player_exists_by_player_id
from DBHelper.tables.player_monster_additional_property_record import add_player_monster_additional_property_record, \
    update_player_monster_additional_property_record
from DBHelper.tables.player_achievement_record import add_player_achievement_record

from Enums import BeingType, AdditionSourceType


class App:
    def __init__(self, player_id: int, nick_name: str):
        super(App, self).__init__()
        self.player_id = player_id
        self.nick_name = nick_name

    def start(self):
        while True:
            player_input = input("请输入您要执行的操作")
            self.handle_player_input(player_input)

    def handle_player_input(self, player_input: str):
        if player_input == '登陆':
            self.handle_player_log_in_game()

    def handle_player_log_in_game(self, ):
        """
        处理玩家进入游戏的函数
        :return:
        """
        if not is_player_exists_by_player_id(self.player_id):
            # 完成新建玩家和玩家对应属性表

            # 新增玩家
            _id = add_player(self.player_id, nickname=self.nick_name, current_level=0, current_experience=0,
                             game_sign="")
            # 新增玩家对应属性表
            add_player_monster_additional_property_record(being_type=BeingType.PLAYER,
                                                          being_id=_id,
                                                          attack_speed=0,
                                                          attack=0,
                                                          health=0,
                                                          health_recovery=0,
                                                          health_absorption=0,
                                                          mana=0,
                                                          mana_recovery=0,
                                                          mana_absorption=0,
                                                          counterattack=0,
                                                          ignore_counterattack=0,
                                                          critical_point=0,
                                                          damage_shield=0,
                                                          )
            # 给新玩家一个新人成就
            add_player_achievement_record(achievement_id=1, character_id=_id, achieve_timestamp=int(time.time()))
            # 给了新的成就之后要更新玩家的属性
            update_player_monster_additional_property_record()
            print("欢迎进入世界！")
            return
        else:
            print(f"欢迎{self.nick_name}回到游戏！")


if __name__ == '__main__':
    app = App(player_id=603997262, nick_name="York")
    app.start()
