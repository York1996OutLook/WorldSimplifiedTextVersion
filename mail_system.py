import time
from collections import defaultdict
from typing import List

from sqlalchemy import Boolean

from DBHelper.db import *

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
    player_mail_record.insert_to_available_position(
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
    one_player = player.get_by_character_id(character_id=character_id)

    one_player_mail_record = player_mail_record.get_by_record_id(record_id=player_mail_record_id)

    # 处理黄金归属
    one_player.gold_num += one_player_mail_record.give
    one_player.gold_num -= one_player_mail_record.charge

    # 如果有物品，则将物品放到背包中。
    if one_player_mail_record.give_stuff_id:
        player_stuff_record.insert_stuff_to_player_bag(stuff_record_id=one_player_mail_record.give_stuff_id,
                                                       character_id=one_player.id)
        one_player_mail_record = player_stuff_record.get_by_record_id(
            record_id=one_player_mail_record.give_stuff_record_id)
        one_player_mail_record.character_id = character_id

    # 删除该邮件
    player_mail_record.delete_by_mail_id(record_id=player_mail_record_id)


# 拒绝某个发给自己的邮件
def reject_a_mail(*,
                  record_id: int
                  ):
    # 邮件发送者会看到这个邮件的状态是被拒收了，并且是未读状态；
    one_player_mail_record = player_mail_record.get_by_record_id(record_id=record_id)
    player_mail_record.update_type_by_record_id(mail_record_id=one_player_mail_record,
                                                new_mail_type=MailType.SEND_TO_OTHER_PLAYER_GET_REJECT)
    player_mail_record.update_read_status(mail_id=one_player_mail_record, is_read=False)
