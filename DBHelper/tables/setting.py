import os
import os.path as osp

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from typing import List

import local_setting
from Utils import tools

Base = declarative_base()

from DBHelper.session import session
from DBHelper.tables.base_table import Entity


class Setting(Entity):
    """
    比如:
    一个人最多可以学习多少个技能,10

    交易所税率 3%
    充值比例  200%
    挂售退回时间  72 hour

    每日可以挑战次数 # 10
    致命伤害的加成:2.5
    每升星的加成

    抽到特定数字会获奖,这个数字是:
    在邮件中,游戏管理员显示的ID
    可以开始打卡的时间,暂定8
    结束可以打卡的时间,暂定10

    """
    __tablename__ = 'setting'

    value = Column(String, comment="设置的值,如果是数字,则将字符串转换为数字;")
    comment = Column(String, comment="注释,备忘录")

    @classmethod
    def add_or_update_by_name(cls,
                              *,
                              name: str,
                              value: str=None,
                              comment: str = None
                              ) -> "Setting":

        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_name)
        record = cls._add_or_update_by_name(**fields)
        return record

    @classmethod
    def add_or_update_by_id(
            cls,
            *,
            _id: int,

            name: str = None,
            value: str = None,
            comment: str = None
            ) -> "Setting":

        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
        return record


# 增


# 删


# 改


# 查
def get_max_battle_round_num() -> int:
    """
    获取最大回合数
    :return:
    """
    value = get_value_by_name(name='max_battle_round_num')
    return int(value)


def get_critical_damage_multiplier():
    """
    :return: 获取致命伤害的翻倍值
    """
    value = get_value_by_name(name='critical_damage_multiplier')
    return float(value)


def get_percent100_mana_absorption():
    """
    :return: 获取致命伤害的翻倍值
    """
    value = get_value_by_name(name='percent100_mana_absorption')
    return float(value)


def get_percent100_health_absorption():
    """
    :return: 获取致命伤害的翻倍值
    """
    value = get_value_by_name(name='percent100_health_absorption')
    return float(value)


def get_percent100_counterattack():
    """
    :return: 获取致命伤害的翻倍值
    """
    value = get_value_by_name(name='percent100_counterattack')
    return float(value)


def get_percent100_critical_point():
    """
    :return: 获取最大致命点，预计为 1000
    """
    value = get_value_by_name(name='full_critical_point')
    return int(value)


# other
def get_per_star_improved_percent() -> int:
    """
    获取每个升星会获得多少加成。
    :return:
    """
    value = get_value_by_name(name='per_star_improved_percent')
    return int(value)


def get_per_level_base_point_num() -> int:
    """
    获取每个升星会获得多少加成。
    :return:
    """
    value = get_value_by_name(name='per_level_base_point_num')
    return int(value)


def get_initial_player_level() -> int:
    """
    获取初始用户初始等级。
    :return:
    """
    value = get_value_by_name(name='initial_player_level')
    return int(value)


def get_player_default_game_sign() -> str:
    """
    获取用户默认签名。
    :return:
    """
    value = get_value_by_name(name='player_default_game_sign')
    return value


# lottery
def get_lottery_start_hour():
    """
    获取开始抽奖的时间
    :return:
    """
    value = get_value_by_name(name='lottery_start_hour')
    return int(value)


def get_lottery_end_hour():
    """
    获取结束抽奖的时间
    :return:
    """
    value = get_value_by_name(name='lottery_end_hour')
    return int(value)


def get_lottery_lucky_num():
    """
    获取结束抽奖的时间
    :return:
    """
    value = get_value_by_name(name='lottery_lucky_num')
    return int(value)


# sell_store
def get_sell_expire_hours():
    """
    获取结束抽奖的时间
    :return:
    """
    value = get_value_by_name(name='sell_expire_hours')
    return int(value)


# game master
def get_game_master_id():
    """
    获取结束抽奖的时间
    :return:
    """
    value = get_value_by_name(name='game_master_id')
    return int(value)


if __name__ == '__main__':
    setting_json_root = osp.join(local_setting.json_data_root, "setting")
    json_files = os.listdir(setting_json_root)
    for json_file in json_files:
        src = osp.join(setting_json_root, json_file)
        setting_dict_list = tools.file2dict_list(src=src)
        for setting_dict in setting_dict_list:
            setting_name = setting_dict['名称']
            setting_value = setting_dict['值']
            setting_comment = setting_dict['备注']
            add_or_update(name=setting_name,
                          value=setting_value,
                          comment=setting_comment,
                          verbose=local_setting.verbose)
