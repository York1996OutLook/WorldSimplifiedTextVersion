import time
from collections import defaultdict
from typing import List

from sqlalchemy import Boolean

from DBHelper.db import *
from Enums import AdditionSourceType, AdditionalPropertyType, BasePropertyType, MailType
from mail_system import send_email
from Utils import tools


# 交易所检查所有过期物品并且退回
def sell_store_return_or_expire_stuffs():
    """

    :return:
    """
    # 从设置中查询过期时间
    sell_expire_hours = setting.get_sell_expire_hours()
    sell_expire_milliseconds = tools.convert_to_milliseconds(hours=sell_expire_hours)

    # 获得当前所有过期的物品，
    expired_sell_store_records = get_expired_records(current_timestamp=int(time.time()),
                                                     expired_milliseconds=sell_expire_milliseconds)

    # 通过邮件的方式退回给玩家
    gm_id = setting.get_game_master_id()
    for expired_sell_store_record in expired_sell_store_records:
        player_stuff_record = get_player_stuff_record_by_record_id(expired_sell_store_record.id)
        stuff = get_stuff_by_stuff_id(player_stuff_record.stuff_id)
        additional_msg = f"""
        未能成功出售！
        物品名称：{stuff.name} x {player_stuff_record.stuff_num}
        挂售时间{tools.timestamp_to_date_string(expired_sell_store_record.initial_sell_timestamp)}
        挂售价格{expired_sell_store_record.original_price}
        """
        send_email(send_character_id=gm_id,
                   received_character_id=expired_sell_store_record.owner_character_id,
                   give_stuff_record_id=expired_sell_store_record.stuff_record_id,
                   charge=0,
                   give=0,
                   mail_type=MailType.RECEIVED_FROM_EXCHANGE_STORE_NOT_SOLD_RETURN,
                   addition_message=additional_msg
                   )

        # 从交易所中删除该记录
        delete_sell_store_record(sell_store_record_id=expired_sell_store_record.stuff_record_id)


# 用户取消 销售某商品之后，物品应该回到邮箱中
def player_cancel_sell_stuff_send_mail(*, player_sell_store_record_id: int, ):
    # 获得取消售出物品的详细信息
    player_sell_store_record = get_sell_store_record_by_record_id(player_sell_store_record_id)
    stuff = get_stuff_by_stuff_id(player_sell_store_record.give_stuff_record_id)
    player_stuff_record = get_player_stuff_record_by_record_id(player_sell_store_record.stuff_record_id)

    additional_msg = f"""
    未售出物品名称：{stuff.name} x {player_stuff_record.stuff_num}

    挂售时间{tools.timestamp_to_date_string(player_sell_store_record.initial_sell_timestamp)}
    取消挂售时间{tools.timestamp_to_date_string(int(time.time()))}
    """

    # 通过邮件的方式退回给玩家
    gm_id = get_game_master_id()
    send_email(send_character_id=gm_id,
               received_character_id=player_sell_store_record.owner_character_id,
               give_stuff_record_id=player_sell_store_record.stuff_record_id,  # 由于已经售出，则收到的邮件中物品栏为空
               charge=0,
               give=0,
               mail_type=MailType.RECEIVED_FROM_EXCHANGE_STORE_POSITIVE_RETURN,
               addition_message=additional_msg
               )

    # 从交易所中删除该记录
    delete_sell_store_record(sell_store_record_id=player_sell_store_record_id)
    return player_sell_store_record


# 购买某物品成功后，物品到买家背包中，所得收益发送到卖家邮箱中
def player_buy_sell_store_stuff_to_self_bag(*, buyer_character_id: int, player_sell_store_record_id: int):
    """

    :param buyer_character_id: 买家
    :param player_sell_store_record_id:
    :return:
    """

    # 获得所买物品的详细信息
    one_player_sell_store_record = player_sell_store_record.get_by_record_id(record_id=player_sell_store_record_id)
    one_stuff = player_stuff_record.get_by_record_id(record_id=one_player_sell_store_record.give_stuff_record_id)



    # 物品售出后，给挂售物品的人发赠送黄金的邮件
    addition_message = f"""
    售出物品名称：{stuff.name} x {player_stuff_record.stuff_num}
    初始挂售时间：{tools.timestamp_to_date_string(one_player_sell_store_record.initial_sell_timestamp)}
    售出时间：{tools.timestamp_to_date_string(int(time.time()))}
    获得黄金：{one_player_sell_store_record.original_price}
    """

    gem_id = setting.get_game_master_id()
    send_email(
        send_character_id=gem_id,
        received_character_id=player_sell_store_record.owner_character_id,
        give_stuff_record_id=0,
        charge=0,
        give=player_sell_store_record.original_price,
        mail_type=MailType.RECEIVED_FROM_EXCHANGE_STORE_SOLD,
        addition_message=addition_message
    )

    # 商品会到买家背包中。不通过邮件发送；
    new_stuff_record = player_stuff_record.insert_stuff_to_player_bag(stuff_record_id=one_player_stuff_record.id,
                                                                      character_id=buyer_character_id)
    msg = f"""
    花费：{player_sell_store_record.taxed_price} 黄金
    购买物品名称：{stuff.name} x {new_stuff_record.stuff_num}
    放到背包位置B{new_stuff_record.position_in_bag}    
    """
    print(msg)

    # 从交易所中删除该记录
    player_stuff_record.delete_sell_store_record(sell_store_record_id=player_sell_store_record_id)
