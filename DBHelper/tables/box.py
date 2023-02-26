import os.path as osp

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from typing import List

from DBHelper.session import session
import local_setting
from Utils import tools

Base = declarative_base()


class Box(Base):
    """
    箱子，一般均可以出售
    """
    __tablename__ = 'box'

    id = Column(Integer, primary_key=True)
    name = Column(String, comment="箱子的中文名字")
    is_bind = Column(Boolean, comment="是否已经绑定")

    introduction = Column(String, comment="说明")

    def __init__(self, *,
                 name: str,
                 is_bind: bool,
                 introduction: str):
        self.name = name
        self.is_bind = is_bind
        self.introduction = introduction


# 增

def add(*,
        name: str,
        is_bind: bool,
        introduction: str
        ) -> Box:
    """
    新增一条记录
    :param name:
    :param is_bind:
    :param introduction:
    :return:
    """
    new_box = Box(name=name, is_bind=is_bind, introduction=introduction)
    session.add(new_box)
    session.commit()
    session.refresh(new_box)
    return new_box


def add_or_update_by_name(*,
                          name: str,
                          is_bind: bool,
                          introduction: str
                          ) -> Box:
    if is_exists_by_name(name=name):
        box = update_by_name(name=name, is_bind=is_bind, introduction=introduction)
    else:
        box = add(name=name, is_bind=is_bind, introduction=introduction)
    return box


# 删

# 改
def update_by_name(*,
                   name: str,
                   is_bind: bool,
                   introduction: str):
    """
    通过名称查询，然后更新；
    :param name:
    :param is_bind:
    :param introduction:
    :return:
    """
    box = session.query(Box).filter_by(name=name).first()
    box.is_bind = is_bind
    box.introduction = introduction
    session.commit()
    session.refresh(box)
    return box


# 查

def is_exists_by_name(*, name: str) -> bool:
    """
    根据名称判断记录是否存在
    :param name:
    :return:
    """
    record = session.query(Box).filter(Box.name == name).first()
    return record is not None


def get_by_name(*, name: str) -> Box:
    """
    根据name获得box
    :param name:
    :return:
    """
    record = session.query(Box).filter(Box.name == name).first()
    return record
