import abc
from abc import ABC, abstractmethod
import inspect
from typing import List, Callable, Dict

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session

Base = declarative_base()


class Basic:
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        """
        add的时候用到
        """
        for k, v in kwargs.items():
            setattr(self, k, v)

    # base
    @classmethod
    def query_one_by_id(cls, *, _id) -> cls:
        """
        仅仅返回查询的第一个对象。如果不存在则返回None
        """
        record = session.query(cls).filter(cls.id == _id).first()
        return record

    @classmethod
    def query_all(cls) -> List[cls]:
        """
        返回查到的所有对象
        """
        records = session.query(cls).all()
        return records

    @classmethod
    def get_all_by(cls, **kwargs) -> List[cls]:
        """
        通过传入字段及值获取所有记录。如果为None则代表对这个字段不筛选
        :param kwargs: 字段及值
        :return: List
        """
        kwargs = {key: kwargs[key] for key in kwargs if kwargs[key] is not None}
        records = session.query(cls).filter_by(**kwargs).all()
        return records

        # 增

    @classmethod
    def add_with_kwargs(cls, **kwargs):
        """
        根据传来的键值对更改
        """
        record = cls(**kwargs)
        session.add(record)
        session.commit()

    # 删
    @classmethod
    def del_by_id(cls, *, _id: int) -> bool:
        """
        如果确实删除成功，则返回true。
        如果被删除的id不存在，则抛出异常
        """
        record = cls.query_one_by_id(_id=_id)
        if record is None:
            raise ValueError(f'id: {_id} 对应的记录不存在！')
        session.delete(record)
        session.commit()
        return True

    @classmethod
    def del_one_by_kwargs(cls, **kwargs) -> bool:
        """
        如果确实删除了数据，则返回true，否则返回false
        """
        record = session.query(cls).filter_by(**kwargs).first()
        session.delete(record)
        session.commit()
        return record is not None

    @classmethod
    def del_all_by_kwargs(cls, **kwargs) -> bool:
        """
        如果确实删除了数据，则返回true，否则返回false
        """
        records = session.query(cls).filter_by(**kwargs).all()
        session.delete(records)
        session.commit()
        return len(records) > 0

    @classmethod
    def del_all(cls) -> bool:
        """
        如果确实删除了数据，则返回true，否则返回false
        """
        records = cls.query_all()
        session.delete(records)
        session.commit()

        return len(records) > 0

    # 改
    @classmethod
    def update_kwargs_by_id(cls, *, _id: int, **kwargs) -> bool:
        """
        如果没有查询到对应的记录，则抛出异常
        """
        record = cls.query_one_by_id(_id=_id)
        if record is None:
            raise ValueError(f'id: {_id} 对应的记录不存在！')
        for k, v in kwargs.items():
            if v is not None:
                setattr(record, k, v)
        return True

    @classmethod
    def update_fields_by_query_dict(cls, *, query_dict: Dict, **update_dict: Dict) -> cls:
        """
        如果没有查询到对应的记录，则抛出异常
        """
        record = cls.get_one_by_kwargs(**query_dict)
        if record is None:
            raise ValueError(f'对应的记录不存在！')
        for k, v in update_dict.items():
            if v is not None:
                setattr(record, k, v)
        return record

    # 查
    @classmethod
    def get_by_id(cls, *, _id: int) -> cls:
        """
        返回查询到的第一个记录，
        如果没有查询到，则返回 None
        """
        record = cls.query_one_by_id(_id=_id)
        return record

    @classmethod
    def get_all_by_range(cls,
                         *,
                         field: str,
                         start: float,
                         end: float
                         ) -> List[cls]:
        """
        区间端点均可以取到
        :param field: 要查询的字段
        :param start: 区间开始
        :param end: 区间结束
        :return: List[RaiseStarProb]
        """
        records = session.query(cls).filter(getattr(cls, field) >= start,
                                            getattr(cls, field) <= end).all()
        return records

    @classmethod
    def get_one_by_kwargs(cls, **kwargs) -> cls:
        """
        返回查询到的第一个记录，
        如果没有查询到，则返回 None
        """
        record = session.query(cls).filter_by(**kwargs).first()
        return record

    @classmethod
    def get_all(cls) -> List[cls]:
        """
        查询所有，如果查询到则返回list，如果没有查询到，则返回空列表
        """
        records: List[cls] = cls.query_all()
        return records

    # exists
    @classmethod
    def is_exists_by_kwargs(cls, **kwargs) -> bool:
        """
        存在则返回true，不存在则返回false
        """
        record = cls.get_one_by_kwargs(kwargs=kwargs)
        return record is not None

    @classmethod
    def is_exists_by_id(cls, *, _id: int) -> bool:
        """
        存在则返回true，不存在则返回false
        """
        record = cls.query_one_by_id(_id=_id)
        return record is not None

    @classmethod
    def _add_or_update_by_id(cls,
                             *,
                             _id: int,
                             **kwargs,
                             ) -> cls:
        """
        返回修改或者新增后的记录
        """
        if cls.is_exists_by_id(_id=_id):
            return cls.update_kwargs_by_id(_id=_id, kwargs=kwargs)
        else:
            return cls.add_with_kwargs(**kwargs)

    @classmethod
    def update_fields_from_signature(cls, *, func: Callable):
        """
        从函数的签名中，自动获取参数的 键值对；
        """
        signature = inspect.signature(func)
        fields = dict()
        for param_name, param in signature.parameters.items():
            if param_name in {'_id'}:
                continue
            fields[param_name] = param.default if param.default is not inspect.Parameter.empty else None
        return fields

    @classmethod
    @abstractmethod
    def add_or_update_by_id(cls, *, _id: int, **kwargs):
        """
        根据id来新增或者更新
        抽象方法，对于继承自他的类来说，这个方法必须被实现
        """
        ...


class Entity(Basic):
    name = Column(String)

    # base
    @classmethod
    def query_one_by_name(cls, *, name: str) -> cls:
        """
        查询到则返回第一个记录，否则返回false
        """
        record = session.query(cls).filter(cls.name == name).first()
        return record

    # 增
    @classmethod
    def add_with_name(cls, *, name: str) -> cls:
        """
        新增一个记录，并且初始化其name属性
        """
        record = cls()
        record.name = name
        session.add(record)
        session.commit()
        return record

    # 删
    @classmethod
    def del_by_name(cls, *, name: str) -> bool:
        """
        根据name进行查询，并且删除name对应的记录
        如果存在则返回true，如果不存在
        """
        record = cls.query_one_by_name(name=name)
        if record is None:
            raise ValueError(f'name: {name} 对应的记录不存在！')
        session.delete(record)
        session.commit()
        return True

    # 改
    @classmethod
    def update_kwargs_by_name(cls, *, name: str, **kwargs) -> cls:
        """
        根据name来查询记录，并且更新一些字段
        如果不存在，则抛出异常
        建议前置判断存在的函数
        """
        record = cls.get_by_name(name=name)
        if record is None:
            raise ValueError(f'name: {name} 对应的记录不存在！')
        for k, v in kwargs.items():
            if v is not None:
                setattr(record, k, v)
        return record

    @classmethod
    def update_name_by_name(cls, *, old_name: str, new_name: str) -> cls:
        """
        根据name来查询记录，并且更新name属性
        如果不存在，则抛出异常
        建议前置判断存在的函数
        """
        record = cls.query_one_by_name(name=old_name)
        if record is None:
            raise ValueError(f'name:{old_name} 对应的记录不存在！')
        record.name = new_name
        session.commit()
        return record

    @classmethod
    def update_name_by_id(cls, *, _id: str, new_name: str) -> cls:
        """
        根据id来查询记录，并且更新name属性
        如果不存在，则抛出异常
        建议前置判断存在的函数
        """
        record = cls.query_one_by_id(_id=_id)
        if record is None:
            raise ValueError(f'ID: {_id} 对应的记录不存在！')
        record.name = new_name
        session.commit()
        return record

    # 查
    @classmethod
    def get_by_name(cls, *, name: str) -> cls:
        """
        根据name进行查询，返回第一条记录
        如果存在则返回true，如果不存在
        """
        record = cls.query_one_by_name(name=name)
        return record

    @classmethod
    def is_exists_by_name(cls, *, name: str) -> cls:
        """
        根据name进行查询
        存在返回true，不存在返回false
        """
        record = cls.query_one_by_name(name=name)
        return record is not None

    @classmethod
    def _add_or_update_by_name(cls,
                               *,
                               name: str,
                               **kwargs,
                               ) -> cls:
        """
        返回新增或者更新后的记录。
        如果update的时候，name不存在，则抛出异常
        """
        if cls.is_exists_by_name(name=name):
            return cls.update_kwargs_by_name(name=name, kwargs=kwargs)
        else:
            return cls.add_with_kwargs(name=name, **kwargs)

    # 虚类
    @classmethod
    @abstractmethod
    def add_or_update_by_id(cls, *, name: str, **kwargs) -> cls:
        """
        返回新增或者更新后的记录。
        """
        ...

    # 虚类
    @classmethod
    @abstractmethod
    def add_or_update_by_name(cls, *, name: str, **kwargs) -> cls:
        """
        强制继承自他的类，必须实现这个方法，如果不实现，也要声明为抽象方法；
        """
        ...
