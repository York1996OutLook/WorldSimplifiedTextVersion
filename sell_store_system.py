import time
from collections import defaultdict
from typing import List

from sqlalchemy import Boolean

from DBHelper.tables.player_achievement_record import get_all_achievements_records_by_character_id
from DBHelper.tables.achievement import get_achievement_by_achievement_id
from DBHelper.tables.skill_achievement_equipment_etc_properties import SkillAchievementEquipmentEtcProperties, \
    get_properties_dict_by_source_type_and_id
from DBHelper.tables.player_skill_record import PlayerSkillRecord, \
    get_player_skill_record_by_character_id_and_skill_id
from DBHelper.tables.skill_book import SkillBook, get_skill_book_by_skill_id_skill_level
from DBHelper.tables.player_stuff_record import PlayerStuffRecord, get_all_wearing_stuffs_by_character_id
from DBHelper.tables.equipment_gem_record import get_all_gems_by_equipment_id
from DBHelper.tables.gem import get_gem_by_gem_id
from DBHelper.tables.setting import get_per_star_improved_percent, get_sell_expire_hours, get_game_master_id
from DBHelper.tables.setting import get_lottery_start_hour, get_lottery_end_hour, get_lottery_lucky_num
from DBHelper.tables.player_lottery_record import get_all_is_lucky_num_player_lottery_records_by_timestamp
from DBHelper.tables.player_lottery_record import get_all_player_lottery_records_with_max_lucky_num_by_timestamp
from DBHelper.tables.player_mail_record import insert_player_mail_record_to_available_position
from DBHelper.tables.player_stuff_record import get_player_stuff_record_by_record_id, add_player_stuff_record, \
    insert_stuff_to_player_bag
from DBHelper.tables.player_sell_store_record import get_sell_store_record_by_record_id, get_expired_records, \
    delete_sell_store_record,PlayerSellStoreRecord
from DBHelper.tables.stuff import get_stuff_by_stuff_id
from mail_system import send_email

from Enums import AdditionSourceType, AdditionalPropertyType, BasePropertyType, MailType
from Utils import tools


# 交易所检查所有过期物品并且退回
def sell_store_return_or_expire_stuffs():
    """

    :return:
    """
    # 从设置中查询过期时间
    sell_expire_hours = get_sell_expire_hours()
    sell_expire_milliseconds = tools.convert_to_milliseconds(hours=sell_expire_hours)

    # 获得当前所有过期的物品，
    expired_sell_store_records = get_expired_records(current_timestamp=int(time.time()),
                                                     expired_milliseconds=sell_expire_milliseconds)

    # 通过邮件的方式退回给玩家
    gm_id = get_game_master_id()
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
def player_cancel_sell_stuff_send_mail(player_sell_store_record_id: int, ):
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
def player_buy_sell_store_stuff_to_self_bag(buyer_character_id: int, player_sell_store_record_id: int):
    """

    :param buyer_character_id: 买家
    :param player_sell_store_record_id:
    :return:
    """

    # 获得所买物品的详细信息
    player_sell_store_record = get_sell_store_record_by_record_id(player_sell_store_record_id)
    stuff = get_stuff_by_stuff_id(player_sell_store_record.give_stuff_record_id)
    player_stuff_record = get_player_stuff_record_by_record_id(player_sell_store_record.stuff_record_id)

    # 物品售出后，给挂售物品的人发赠送黄金的邮件
    addition_message = f"""
    售出物品名称：{stuff.name} x {player_stuff_record.stuff_num}
    初始挂售时间：{tools.timestamp_to_date_string(player_sell_store_record.initial_sell_timestamp)}
    售出时间：{tools.timestamp_to_date_string(int(time.time()))}
    获得黄金：{player_sell_store_record.original_price}
    """

    gem_id = get_game_master_id()
    send_email(
        send_character_id=gem_id,
        received_character_id=player_sell_store_record.owner_character_id,
        give_stuff_record_id=None,
        charge=0,
        give=player_sell_store_record.original_price,
        mail_type=MailType.RECEIVED_FROM_EXCHANGE_STORE_SOLD,
        addition_message=addition_message
    )

    # 商品会到买家背包中。不通过邮件发送；
    new_stuff_record = insert_stuff_to_player_bag(stuff_record_id=player_stuff_record.id,
                                                  character_id=buyer_character_id)
    msg = f"""
    花费：{player_sell_store_record.taxed_price} 黄金
    购买物品名称：{stuff.name} x {new_stuff_record.stuff_num}
    放到背包位置B{new_stuff_record.position_in_bag}    
    """
    print(msg)

    # 从交易所中删除该记录
    delete_sell_store_record(sell_store_record_id=player_sell_store_record_id)

