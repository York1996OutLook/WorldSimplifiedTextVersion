from typing import List

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session
from DBHelper.tables.base_table import Basic,Base


class RaiseStarProb(Basic,Base):
    """
    升星概率表

    """
    __tablename__ = 'raise_star_prob'

    star_count = Column(Integer, comment="当前升星数量")
    success_prob = Column(Integer, comment="从上一星星数量升级到当前数量的星星成功的概率,100为决定成功,0是无法成功")

    @classmethod
    def add_or_update_by_id(cls,
                            *,
                            _id: int = None,
                            star_count: int = None,
                            success_prob: int = None
                            ):
        """
        更新或创建升星概率记录
        :param _id: 记录ID
        :param star_count: 当前升星数量
        :param success_prob: 从上一星星数量升级到当前数量的星星成功的概率,100为决定成功,0是无法成功
        :return:
        """
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
        return record

    @classmethod
    def get_by_star_count(cls, star_count: int) -> "RaiseStarProb":
        """
        通过星星数量获取升星概率记录
        :param star_count: 星星数量
        :return: RaiseStarProb
        """
        record=cls.get_one_by_kwargs(star_count=star_count)
        return record


# 增
# 删
# 改
def update_success_prob_by_start_count(*,
                                       star_count: str,
                                       success_prob: str
                                       ) -> RaiseStarProb:
    """
    更新升星概率记录
    :param star_count: 当前升星数量
    :param success_prob: 从上一星星数量升级到当前数量的星星成功的概率，100为决定成功，0是无法成功
    :return: RaiseStarProb object
    """
    raise_star_prob = session.query(RaiseStarProb).filter(RaiseStarProb.star_count == star_count).first()
    raise_star_prob.success_prob = success_prob
    session.commit()
    session.refresh(raise_star_prob)
    return raise_star_prob


# 查
def is_exists_by_star_count(*,
                            star_count: int
                            ) -> bool:
    """
    根据star_count判断升星概率记录是否存在
    """
    record = session.query(RaiseStarProb.star_count == star_count).first()
    return record is not None


def get_success_prob_by_star_count(*,
                                   star_count: int
                                   ) -> str:
    """
    根据升星数量查询成功概率

    :param star_count: 升星数量
    :return: 成功概率
    """

    prob = session.query(RaiseStarProb).filter_by(star_count=star_count).first()
    return prob.success_prob


if __name__ == '__main__':
    """
    具体的数值要参考，有一个值为1的属性，每次升星比例是3%，也就是升星34次之后，会变成2。要求达到33星，不是太难。
    """
    new_probs = [
        {"star_count": 1, "success_prob": 100},
        {"star_count": 2, "success_prob": 100},
        {"star_count": 3, "success_prob": 100},
        {"star_count": 4, "success_prob": 100},
        {"star_count": 5, "success_prob": 100},
        {"star_count": 6, "success_prob": 97},
        {"star_count": 7, "success_prob": 94},
        {"star_count": 8, "success_prob": 91},
        {"star_count": 9, "success_prob": 88},
        {"star_count": 10, "success_prob": 85},
        {"star_count": 11, "success_prob": 82},
        {"star_count": 12, "success_prob": 79},
        {"star_count": 13, "success_prob": 76},
        {"star_count": 14, "success_prob": 73},
        {"star_count": 15, "success_prob": 70},
        {"star_count": 16, "success_prob": 67},
        {"star_count": 17, "success_prob": 64},
        {"star_count": 18, "success_prob": 61},
        {"star_count": 19, "success_prob": 58},
        {"star_count": 20, "success_prob": 55},
        {"star_count": 21, "success_prob": 52},
        {"star_count": 22, "success_prob": 49},
        {"star_count": 23, "success_prob": 46},
        {"star_count": 24, "success_prob": 43},
        {"star_count": 25, "success_prob": 40},
        {"star_count": 26, "success_prob": 37},
        {"star_count": 27, "success_prob": 34},
        {"star_count": 28, "success_prob": 31},
        {"star_count": 29, "success_prob": 28},
        {"star_count": 30, "success_prob": 25},
        {"star_count": 31, "success_prob": 22},
        {"star_count": 32, "success_prob": 19},
        {"star_count": 33, "success_prob": 16},
        {"star_count": 34, "success_prob": 13},
        {"star_count": 35, "success_prob": 10},
        {"star_count": 36, "success_prob": 7},
        {"star_count": 37, "success_prob": 4},
        {"star_count": 38, "success_prob": 1},
        {"star_count": 39, "success_prob": 1},
        {"star_count": 40, "success_prob": 1},
        {"star_count": 41, "success_prob": 1},
        {"star_count": 42, "success_prob": 1},
        {"star_count": 43, "success_prob": 1},
        {"star_count": 44, "success_prob": 1},
        {"star_count": 45, "success_prob": 1},
        {"star_count": 46, "success_prob": 1},
        {"star_count": 47, "success_prob": 1},
        {"star_count": 48, "success_prob": 1},
        {"star_count": 49, "success_prob": 1},
        {"star_count": 50, "success_prob": 1},
        {"star_count": 51, "success_prob": 0},
    ]

    for one_prob in new_probs:
        add_or_update(star_count=one_prob['star_count'], success_prob=one_prob['success_prob'])
        print(f"star_count: {one_prob['star_count']}, success_prob: {one_prob['success_prob']}")
