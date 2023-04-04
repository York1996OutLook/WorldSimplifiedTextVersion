import os.path as osp

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Optional

import local_setting
from DBHelper.session import session
from Enums import ExpBookType, exp_book_cn_type_dict
from Utils import tools

Base = declarative_base()


class ExpBook(Base):
    """
    经验的列表
    """
    __tablename__ = 'exp_book'
    id = Column(Integer, primary_key=True)
    exp_book_name = Column(String, comment="经验书的名字")
    exp_book_type = Column(Integer, comment="经验书的类型，目前只有一种：人物")
    exp_value = Column(Integer, comment="技能书的等级，高等级技能书可以学习低等级技能，但是反过来不行")

    is_bind = Column(Boolean, comment="刚出来的时候是否已经绑定")

    def __init__(self, *, exp_book_name: str, exp_book_type: ExpBookType, exp_value: int, is_bind: bool):
        self.exp_book_name = exp_book_name
        self.exp_book_type = exp_book_type
        self.exp_value = exp_value
        self.is_bind = is_bind


# 增
def add(*,
        exp_book_name: str,
        exp_book_type: ExpBookType,
        exp_value: int,
        is_bind: bool
        ) -> ExpBook:
    exp_book = ExpBook(exp_book_name=exp_book_name, exp_book_type=exp_book_type, exp_value=exp_value, is_bind=is_bind)
    session.add(exp_book)
    session.commit()
    session.refresh(exp_book)
    return exp_book


def add_or_update_by_name(*,
                          exp_book_name: str,
                          exp_book_type: ExpBookType,
                          exp_value: int,
                          is_bind: bool
                          ) -> ExpBook:
    if is_exists_by_name(name=exp_book_name):
        return update_by_name(exp_book_name=exp_book_name,
                              exp_book_type=exp_book_type,
                              exp_value=exp_value,
                              is_bind=is_bind)
    else:
        return add(exp_book_name=exp_book_name,
                   exp_book_type=exp_book_type,
                   exp_value=exp_value,
                   is_bind=is_bind)


# 删

# 改


def update_by_name(*,
                   exp_book_name: str,
                   exp_book_type: ExpBookType,
                   exp_value: int,
                   is_bind: bool
                   ) -> ExpBook:
    """

    :param exp_book_name:
    :param exp_book_type:
    :param exp_value:
    :param is_bind:
    :return:
    """
    exp_book = session.query(ExpBook).filter(ExpBook.exp_book_name == exp_book_name).first()
    exp_book.exp_book_type = exp_book_type
    exp_book.exp_value = exp_value
    exp_book.is_bind = is_bind
    session.commit()
    session.refresh(exp_book)
    return exp_book


# 查
def is_exists_by_name(*, name: str):
    exp_book = session.query(ExpBook).filter(ExpBook.exp_book_name == name).first()
    return exp_book is not None


def get_by_name(*, name: str) -> ExpBook:
    exp_book = session.query(ExpBook).filter(ExpBook.exp_book_name == name).first()
    return exp_book


def get_by_id(*, _id: int) -> ExpBook:
    exp_book = session.query(ExpBook).filter(ExpBook.id == _id).first()
    return exp_book


if __name__ == '__main__':
    exp_book_json_src = osp.join(local_setting.json_data_root, "book", 'exp_book.json')
    exp_book_dict_list = tools.file2dict_list(src=exp_book_json_src)
    for exp_book_dict in exp_book_dict_list:
        one_name = exp_book_dict['名称']
        one_type_cn = exp_book_dict['类型']
        one_type = exp_book_cn_type_dict[one_type_cn]
        exp_value = exp_book_dict['经验值']

        add_or_update_by_name(exp_book_name=one_name, exp_book_type=ExpBookType.CHARACTER, exp_value=exp_value)
