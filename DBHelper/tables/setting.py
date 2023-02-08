from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from typing import List

Base = declarative_base()

from ..session import session


class Setting(Base):
    """
    比如：
    一个人最多可以学习多少个技能，10

    交易所税率 3%
    充值比例  200%
    挂售退回时间  2day

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


# 增
def add_setting(name: str, value: str) -> Setting:
    """
    新增一个设置

    :param name: 设置的名称
    :param value: 设置的值，字符串类型
    :return: None
    """
    new_setting = Setting(name=name, value=value)
    session.add(new_setting)
    session.commit()
    return new_setting


# 删
def delete_setting(name: str):
    """删除设置

    Args:
        name (str): 要删除的设置名称

    Returns:
        None
    """
    setting = session.query(Setting).filter_by(name=name).first()
    if setting:
        session.delete(setting)


def delete_setting_by_id(setting_id: int):
    """
    根据id删除设置记录

    :param setting_id: 记录的id
    :return: None
    """
    setting = session.query(Setting).filter(Setting.id == setting_id).first()
    if setting:
        session.delete(setting)
        session.commit()


# 改

def update_setting(setting_id: int, new_name: str, new_value: str) -> None:
    """
    Update a single record in the 'setting' table based on its id.

    Args:
        setting_id (int): The id of the setting to update.
        new_name (str): The new name of the setting.
        new_value (str): The new value of the setting.

    Raises:
        ValueError: If the setting with the specified id does not exist.
    """

    # Query the setting with the specified id
    setting = session.query(Setting).get(setting_id)

    # Check if the setting exists
    if setting is None:
        raise ValueError(f"Setting with id {setting_id} does not exist.")

    # Update the setting
    setting.name = new_name
    setting.value = new_value

    # Commit the changes to the database
    session.commit()


# 查
def get_settings() -> list:
    """
    Retrieve all records from the 'setting' table.

    Returns:
        list: A list of dictionaries, where each dictionary represents a setting record and contains keys 'name' and 'value'.
    """
    # Query all records from the 'setting' table
    settings = session.query(Setting).all()

    # Return the result
    return settings


def setting_exists(setting_name: str) -> bool:
    """
    Check if a setting exists in the 'setting' table based on its name.

    Args:
        setting_name (str): The name of the setting to check.

    Returns:
        bool: True if the setting exists, False otherwise.
    """
    # Create a SQLAlchemy engine that connects to the database file
    # Query the setting with the specified name
    setting = session.query(Setting).filter_by(name=setting_name).first()

    # Return the result
    return setting is not None


def get_setting_by_id(setting_id: int) -> Setting:
    """
    Retrieve a single record from the 'setting' table based on its id.

    Args:
        setting_id (int): The id of the setting to retrieve.

    Returns:
        dict: A dictionary that represents the setting record and contains keys 'name' and 'value'.

    Raises:
        ValueError: If the setting with the specified id does not exist.
    """
    # Query the setting with the specified id
    setting = session.query(Setting).get(setting_id)

    # Check if the setting exists
    if setting is None:
        raise ValueError(f"Setting with id {setting_id} does not exist.")

    # Return the result
    return setting


def get_setting_value_by_name(setting_name: str) -> dict:
    """
    Retrieve a single record from the 'setting' table based on its name.

    Args:
        setting_name (str): The name of the setting to retrieve.

    Returns:
        dict: A dictionary that represents the setting record and contains keys 'name' and 'value'.

    Raises:
        ValueError: If the setting with the specified name does not exist.
    """

    # Query the setting with the specified name
    setting = session.query(Setting).filter_by(name=setting_name).first()

    # Check if the setting exists
    if setting is None:
        raise ValueError(f"Setting with name '{setting_name}' does not exist.")

    return setting.value


# other

def get_per_star_improved_percent():
    """
    获取每个升星会获得多少加成。
    :return:
    """
    return get_setting_value_by_name('per_star_improved_percent')

def get_lottery_start_hour():
    """
    获取开始抽奖的时间
    :return:
    """
    return get_setting_value_by_name('lottery_start_hour')

def get_lottery_end_hour():
    """
    获取结束抽奖的时间
    :return:
    """
    return get_setting_value_by_name('lottery_end_hour')

def get_lottery_lucky_num():
    """
    获取结束抽奖的时间
    :return:
    """
    return get_setting_value_by_name('lottery_lucky_num')