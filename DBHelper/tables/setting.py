from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from typing import List

Base = declarative_base()

from DBHelper.session import session


class Setting(Base):
    """
    比如：
    一个人最多可以学习多少个技能，10

    交易所税率 3%
    充值比例  200%
    挂售退回时间  72 hour

    每日可以挑战次数 # 10
    致命伤害的加成：2.5
    每升星的加成

    抽到特定数字会获奖，这个数字是：
    在邮件中，游戏管理员显示的ID
    可以开始打卡的时间，暂定8
    结束可以打卡的时间，暂定10

    """
    __tablename__ = 'setting'

    id = Column(Integer, primary_key=True)
    name = Column(String, comment="设置的名称")
    value = Column(String, comment="设置的值，如果是数字，则将字符串转换为数字；")
    comment = Column(String, comment="注释，备忘录")


# 增
def add_setting(*,
                name: str,
                value: str,
                comment: str,
                ) -> Setting:
    """
    新增一个设置

    :param name: 设置的名称
    :param value: 设置的值，字符串类型
    :param comment: 备忘录
    :return: None
    """
    new_setting = Setting(name=name, value=value, comment=comment)
    session.add(new_setting)
    session.commit()
    return new_setting


def add_or_update(*,
                  name: str,
                  value: str,
                  comment: str, ):
    if is_exist_by_name(name=name):
        setting = update_setting_by_name(name=name, new_value=value, new_comment=comment)
    else:
        setting = add_setting(name=name, value=value, comment=comment)
    return setting


# 删
def delete_setting(*,
                   name: str):
    """删除设置

    Args:
        name (str): 要删除的设置名称

    Returns:
        None
    """
    setting = session.query(Setting).filter_by(name=name).first()
    session.delete(setting)


def delete_setting_by_id(*,
                         setting_id: int
                         ):
    """
    根据id删除设置记录

    :param setting_id: 记录的id
    :return: None
    """
    setting = session.query(Setting).filter(Setting.id == setting_id).first()
    session.delete(setting)
    session.commit()


# 改

def update_setting_by_name(*,
                           name: str,
                           new_value: str,
                           new_comment: str,
                           ) -> Setting:
    """
    Update a single record in the 'setting' table based on its id.

    Args:
        name (str): The new name of the setting.
        new_value (str): The new value of the setting.
        new_comment (str): The new value of the setting.

    """

    # Query the setting with the specified id
    setting = session.query(Setting).filter(Setting.name == name).first()

    # Update the setting
    setting.value = new_value
    setting.new_comment = new_comment

    # Commit the changes to the database
    session.commit()
    return setting


def update_setting_by_setting_name(*,
                                   name: str,
                                   new_value: str = None,
                                   new_comment: str = None,
                                   ) -> Setting:
    """
    Update a single record in the 'setting' table based on its id.

    Args:
        name (str): The new name of the setting.
        new_value (str): The new value of the setting.
        new_comment (str): The new value of the setting.

    """

    # Query the setting with the specified id
    setting = get_setting_by_name(setting_name=name)

    # Update the setting
    setting.value = new_value
    setting.comment = new_comment

    # Commit the changes to the database
    session.commit()
    return setting


# 查
def get_settings() -> List[Setting]:
    """
    Retrieve all records from the 'setting' table.

    Returns:
        list: A list of dictionaries, where each dictionary represents a setting record and contains keys 'name' and 'value'.
    """
    # Query all records from the 'setting' table
    settings = session.query(Setting).all()

    # Return the result
    return settings


def setting_exists(*,
                   setting_name: str
                   ) -> bool:
    """
    Check if a setting exists in the 'setting' table based on its name.

    Args:
        setting_name (str): The name of the setting to check.

    Returns:
        bool: True if the setting exists, False otherwise.
    """
    # Query the setting with the specified name
    setting = session.query(Setting).filter_by(name=setting_name).first()

    # Return the result
    return setting is not None


def get_setting_by_id(*,
                      setting_id: int
                      ) -> Setting:
    """
    Retrieve a single record from the 'setting' table based on its id.

    Args:
        setting_id (int): The id of the setting to retrieve.

    Returns:
        dict: A dictionary that represents the setting record and contains keys 'name' and 'value'.

    """
    # Query the setting with the specified id
    setting = session.query(Setting).get(setting_id)

    # Return the result
    return setting


def get_setting_by_name(*,
                        setting_name: str
                        ) -> Setting:
    """
    Retrieve a single record from the 'setting' table based on its name.

    Args:
        setting_name (str): The name of the setting to retrieve.

    Returns:
        s: A dictionary that represents the setting record and contains keys 'name' and 'value'.

    """

    # Query the setting with the specified name
    setting = session.query(Setting).filter_by(name=setting_name).first()

    return setting


def get_setting_value_by_name(*,
                              setting_name: str
                              ) -> str:
    """
    Retrieve a single record from the 'setting' table based on its name.

    Args:
        setting_name (str): The name of the setting to retrieve.

    Returns:
        dict: A dictionary that represents the setting record and contains keys 'name' and 'value'.

    """

    # Query the setting with the specified name
    setting = session.query(Setting).filter_by(name=setting_name).first()

    return setting.value


def is_exist_by_name(*,
                     name: str
                     ) -> bool:
    setting = session.query(Setting).filter_by(name=name).first()
    return setting is not None


# other

def get_per_star_improved_percent() -> int:
    """
    获取每个升星会获得多少加成。
    :return:
    """
    value = get_setting_value_by_name(setting_name='per_star_improved_percent')
    return int(value)


def get_per_level_base_point_num() -> int:
    """
    获取每个升星会获得多少加成。
    :return:
    """
    value = get_setting_value_by_name(setting_name='per_level_base_point_num')
    return int(value)


def get_initial_player_level() -> int:
    """
    获取每个升星会获得多少加成。
    :return:
    """
    value = get_setting_value_by_name(setting_name='initial_player_level')
    return int(value)


def get_player_default_game_sign() -> str:
    """
    获取每个升星会获得多少加成。
    :return:
    """
    value = get_setting_value_by_name(setting_name='player_default_game_sign')
    return value


def get_lottery_start_hour():
    """
    获取开始抽奖的时间
    :return:
    """
    value = get_setting_value_by_name(setting_name='lottery_start_hour')
    return int(value)


def get_lottery_end_hour():
    """
    获取结束抽奖的时间
    :return:
    """
    value = get_setting_value_by_name(setting_name='lottery_end_hour')
    return int(value)


def get_lottery_lucky_num():
    """
    获取结束抽奖的时间
    :return:
    """
    value = get_setting_value_by_name(setting_name='lottery_lucky_num')
    return int(value)


# sell_store
def get_sell_expire_hours():
    """
    获取结束抽奖的时间
    :return:
    """
    value = get_setting_value_by_name(setting_name='sell_expire_hours')
    return int(value)


# game master
def get_game_master_id():
    """
    获取结束抽奖的时间
    :return:
    """
    value = get_setting_value_by_name(setting_name='game_master_id')
    return int(value)


def get_full_critical_point():
    """
    :return: 获取最大致命点，预计为 1000
    """
    value = get_setting_value_by_name(setting_name='full_critical_point')
    return int(value)


if __name__ == '__main__':
    settings = [
        {
            "name": "full_critical_point",
            "value": 1000,
            "comment": "满致命点的数量，如果实际致命点是100，则10%几率触发暴击。",
        },
        {
            "name": "game_master_id",
            "value": -1,
            "comment": "发邮件的时候所显示的id",
        },
        {
            "name": "sell_expire_hours",
            "value": 72,
            "comment": "交易所挂售物品过期时间",
        },
        {
            "name": "lottery_lucky_num",
            "value": 666,
            "comment": "每日抽奖的幸运数字",
        },
        {
            "name": "lottery_start_hour",
            "value": 1000,
            "comment": "抽奖的开始时间",
        },
        {
            "name": "lottery_end_hour",
            "value": 22,
            "comment": "抽奖的结束时间",
        },
        {
            "name": "player_default_game_sign",
            "value": "玩家很懒，什么都没有留下。。。",
            "comment": "玩家默认的签名信息",
        },
        {
            "name": "initial_player_level",
            "value": 1,
            "comment": "玩家初始的等级",
        },
        {
            "name": "per_star_improved_percent",
            "value": 3,
            "comment": "装备每升一星，装备性能提升多少。",
        },
        {
            "name": "per_level_base_point_num",
            "value": 3,
            "comment": "玩家每升一级，会奖励多少基础属性点",
        }
    ]

    for setting_dic in settings:
        add_or_update(name=setting_dic['name'],
                      value=setting_dic['value'],
                      comment=setting_dic['comment'])
