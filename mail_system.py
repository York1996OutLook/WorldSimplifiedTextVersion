import time
from collections import defaultdict
from typing import List

from sqlalchemy import Boolean

from DBHelper.tables.player_achievement_record import get_all_achievements_records_by_character_id
from DBHelper.tables.achievement import get_achievement_by_achievement_id
from DBHelper.tables.skill_achievement_equipment_etc_properties import SkillAchievementEquipmentEtcProperties, \
    get_properties_dict_by_source_type_and_id
from DBHelper.tables.player_stuff_record import insert_stuff_to_player_bag
from DBHelper.tables.player import get_player_by_player_id, get_player_by_character_id
from DBHelper.tables.player_skill_record import PlayerSkillRecord, \
    get_player_skill_record_by_character_id_and_skill_id
from DBHelper.tables.skill_book import SkillBook, get_skill_book_by_skill_id_skill_level
from DBHelper.tables.player_stuff_record import PlayerStuffRecord, get_all_wearing_stuffs_by_character_id
from DBHelper.tables.equipment_gem_record import get_all_gems_by_equipment_id
from DBHelper.tables.gem import get_gem_by_gem_id
from DBHelper.tables.setting import get_per_star_improved_percent
from DBHelper.tables.setting import get_lottery_start_hour, get_lottery_end_hour, get_lottery_lucky_num
from DBHelper.tables.player_lottery_record import get_all_is_lucky_num_player_lottery_records_by_timestamp
from DBHelper.tables.player_lottery_record import get_all_player_lottery_records_with_max_lucky_num_by_timestamp
from DBHelper.tables.player_mail_record import update_mail_read_status, update_mail_type_by_mail_record_id, \
    insert_player_mail_record_to_available_position, delete_player_mail_record_by_mail_id, \
    get_player_mail_record_by_player_mail_record_id
from DBHelper.tables.stuff import get_stuff_by_stuff_id
from DBHelper.tables.player_stuff_record import get_player_stuff_record_by_record_id

from Enums import AdditionSourceType, AdditionalPropertyType, BasePropertyType, MailType
from Utils import tools


def send_email(
        *,
        send_character_id: int,
        received_character_id: int,
        give_stuff_record_id: int,
        charge: int,
        give: int,
        mail_type: int,
        addition_message: str,
):
    insert_player_mail_record_to_available_position(
        send_character_id=send_character_id,
        received_character_id=received_character_id,
        give_stuff_id=give_stuff_record_id,
        charge=charge,
        give=give,
        mail_type=mail_type,
        is_already_read=False,  # 刚发的邮件都是未读
        addition_message=addition_message,
        send_timestamp=int(time.time()),
    )


# 通过邮件将背包中的物品发送给其它玩家；
def send_bag_stuff_to_other_player(*,
                                   send_character_id: int,
                                   bag_stuff_id: int,
                                   received_character_id: int,
                                   charge: int,
                                   give: int
                                   ):
    # 首先，这个邮件会发送给自己。在对方未查收之前，这个邮件会一直存在；
    send_email(
        send_character_id=send_character_id,
        received_character_id=received_character_id,
        give_stuff_record_id=bag_stuff_id,
        charge=charge,
        give=give,
        mail_type=MailType.SEND_TO_OTHER_PLAYER,
        addition_message=""
    )

    # 其次这个邮件会发送给接受邮件的人。
    send_email(
        send_character_id=send_character_id,
        received_character_id=received_character_id,
        give_stuff_record_id=bag_stuff_id,
        charge=charge,
        give=give,
        mail_type=MailType.SEND_TO_OTHER_PLAYER,
        addition_message=""
    )


# 接受某个发给自己的邮件
def accept_a_mail(*,
                  character_id: int,
                  player_mail_record_id: int
                  ):
    player = get_player_by_character_id(character_id)

    player_mail_record = get_player_mail_record_by_player_mail_record_id(player_mail_record_id)

    # 处理黄金归属
    player.gold_num += player_mail_record.give
    player.gold_num -= player_mail_record.charge

    # 如果有物品，则将物品放到背包中。
    if player_mail_record.give_stuff_id:
        insert_stuff_to_player_bag(player_mail_record.give_stuff_id, character_id=player.id)
        player_stuff_record = get_player_stuff_record_by_record_id(record_id=player_mail_record.give_stuff_record_id)
        player_stuff_record.character_id = character_id

    # 删除该邮件
    delete_player_mail_record_by_mail_id(player_mail_record_id)


# 拒绝某个发给自己的邮件
def reject_a_mail(*,
                  player_mail_record_id: int
                  ):
    # 邮件发送者会看到这个邮件的状态是被拒收了，并且是未读状态；
    player_mail_record = get_player_mail_record_by_player_mail_record_id(player_mail_record_id)
    update_mail_type_by_mail_record_id(player_mail_record, new_mail_type=MailType.SEND_TO_OTHER_PLAYER_GET_REJECT)
    update_mail_read_status(player_mail_record, is_read=False)
