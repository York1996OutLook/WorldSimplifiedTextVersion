from abc import ABC, abstractmethod
import inspect
from typing import List, Callable, Dict, Any, Set

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.session import session

Base = declarative_base()


class MultiLineText(Text):
    ...


class Timestamp(Integer):
    ...


def remove_none_and_cls_kwargs(*,
                               kwargs: Dict[str, Any]
                               ) -> Dict[str, Any]:
    """
    去掉值为空的键值对，并且去除key在other集合中的键值对
    """
    kwargs = {key: kwargs[key] for key in kwargs if kwargs[key] is not None}
    kwargs = {key: kwargs[key] for key in kwargs if key != "cls"}

    return kwargs


class CustomColumn(Column):
    def unique_params(self, *optionaldict, **kwargs):
        pass

    def params(self, *optionaldict, **kwargs):
        pass

    def __init__(self,
                 *args,
                 bind_type=None,
                 cn: str = None,
                 bind_table: str = None,
                 editable: bool = True,
                 **kwargs):
        super(CustomColumn, self).__init__(*args, **kwargs)
        self.bind_type = bind_type
        self.bind_table = bind_table
        self.cn = cn
        self.editable = editable


class Basic:
    id = CustomColumn(Integer,
                      cn='ID',
                      editable=False,
                      primary_key=True)

    # def __init__(self, *, kwargs: Dict[str, Any]):
    #     """
    #     add的时候用到
    #     """
    #     self.__cn__ = ""
    #
    #     for k, v in kwargs.items():
    #         setattr(self, k, v)

    # base
    @classmethod
    def query_one_by_id(cls,
                        *,
                        _id
                        ) -> "cls":
        """
        仅仅返回查询的第一个对象。如果不存在则返回None
        """
        record = session.query(cls).filter(cls.id == _id).first()
        return record

    @classmethod
    def query_all(cls
                  ) -> List['cls']:
        """
        返回查到的所有对象
        """
        records = session.query(cls).all()
        return records

    @classmethod
    def get_all_by_kwargs(cls,
                          *,
                          kwargs: Dict[str, Any]
                          ) -> List['cls']:
        """
        通过传入字段及值获取所有记录。如果为None则代表对这个字段不筛选
        :param kwargs: 字段及值
        :return: List
        """
        kwargs = remove_none_and_cls_kwargs(kwargs=kwargs)
        records = session.query(cls).filter_by(**kwargs).all()
        return records

        # 增

    @classmethod
    def add_with_kwargs(cls,
                        *,
                        kwargs: Dict[str, Any]
                        ) -> 'cls':
        """
        根据传来的键值对更改
        """
        kwargs = remove_none_and_cls_kwargs(kwargs=kwargs)
        record = cls()
        for k, v in kwargs.items():
            setattr(record, k, v)
        session.add(record)
        session.commit()
        return record

    # 删
    @classmethod
    def del_by_id(cls,
                  *,
                  _id: int
                  ) -> bool:
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
    def del_one_by_kwargs(cls,
                          kwargs: Dict[str, Any]
                          ) -> bool:
        """
        如果确实删除了数据，则返回true，否则返回false
        """
        kwargs = remove_none_and_cls_kwargs(kwargs=kwargs)

        record = session.query(cls).filter_by(**kwargs).first()
        session.delete(record)
        session.commit()
        return record is not None

    @classmethod
    def del_all_by_kwargs(cls,
                          kwargs: Dict[str, Any]
                          ) -> bool:
        """
        如果确实删除了数据，则返回true，否则返回false
        """
        kwargs = remove_none_and_cls_kwargs(kwargs=kwargs)

        records = session.query(cls).filter_by(**kwargs).all()
        if len(records) > 0:
            for record in records:
                session.delete(record)
            session.commit()
        return len(records) > 0

    @classmethod
    def del_all(cls
                ) -> bool:
        """
        如果确实删除了数据，则返回true，否则返回false
        """
        records = cls.query_all()
        session.delete(records)
        session.commit()

        return len(records) > 0

    # 改
    @classmethod
    def update_kwargs_by_id(cls,
                            *,
                            _id: int,
                            kwargs: Dict[str, Any]
                            ) -> bool:
        """
        如果没有查询到对应的记录，则抛出异常
        """
        kwargs = remove_none_and_cls_kwargs(kwargs=kwargs)

        record = cls.query_one_by_id(_id=_id)
        if record is None:
            raise ValueError(f'id: {_id} 对应的记录不存在！')
        for k, v in kwargs.items():
            setattr(record, k, v)
        session.commit()
        return True

    @classmethod
    def update_fields_by_query_dict(cls,
                                    *,
                                    query_dict: Dict[str, Any],
                                    **update_dict: Dict[str, Any]
                                    ) -> 'cls':
        """
        如果没有查询到对应的记录，则抛出异常
        """
        update_dict = remove_none_and_cls_kwargs(kwargs=update_dict)

        record = cls.get_one_by_kwargs(**query_dict)
        if record is None:
            raise ValueError(f'对应的记录不存在！')
        for k, v in update_dict.items():
            setattr(record, k, v)
        session.commit()
        return record

    # 查
    @classmethod
    def get_by_id(cls,
                  *,
                  _id: int
                  ) -> 'cls':
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
                         ) -> List['cls']:
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
    def get_one_by_kwargs(cls,
                          kwargs: Dict[str, Any]
                          ) -> 'cls':
        """
        返回查询到的第一个记录，
        如果没有查询到，则返回 None
        """
        kwargs = remove_none_and_cls_kwargs(kwargs=kwargs)
        record = session.query(cls).filter_by(**kwargs).first()
        return record

    @classmethod
    def get_all(cls
                ) -> List['cls']:
        """
        查询所有，如果查询到则返回list，如果没有查询到，则返回空列表
        """
        records: List['cls'] = cls.query_all()
        return records

    # exists
    @classmethod
    def is_exists_by_kwargs(cls,
                            kwargs: Dict[str, Any]
                            ) -> bool:
        """
        存在则返回true，不存在则返回false
        """
        kwargs = remove_none_and_cls_kwargs(kwargs=kwargs)

        record = cls.get_one_by_kwargs(kwargs=kwargs)
        return record is not None

    @classmethod
    def is_exists_by_id(cls,
                        *,
                        _id: int) -> bool:
        """
        存在则返回true，不存在则返回false
        """
        record = cls.query_one_by_id(_id=_id)
        return record is not None

    @classmethod
    def _add_or_update_by_id(cls,
                             *,
                             kwargs: Dict[str, Any],
                             ) -> 'cls':
        """
        返回修改或者新增后的记录
        """
        _id = kwargs['_id']
        kwargs.pop("_id")
        if cls.is_exists_by_id(_id=_id):
            return cls.update_kwargs_by_id(_id=_id, kwargs=kwargs)
        else:
            return cls.add_with_kwargs(**kwargs)

    @classmethod
    @abstractmethod
    def add_or_update_by_id(cls,
                            *,
                            _id: int,
                            kwargs: Dict[str, Any]
                            ) -> "cls":
        """
        根据id来新增或者更新
        抽象方法，对于继承自他的类来说，这个方法必须被实现
        """
        ...


class Entity(Basic):
    name = CustomColumn(Text, cn='名称')

    def __init__(self):
        super(Entity, self).__init__()

    # base
    @classmethod
    def query_one_by_name(cls,
                          *,
                          name: str
                          ) -> 'cls':
        """
        查询到则返回第一个记录，否则返回false
        """
        record = session.query(cls).filter(cls.name == name).first()
        return record

    # 增
    @classmethod
    def add_with_name(cls,
                      *,
                      name: str
                      ) -> 'cls':
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
    def del_by_name(cls,
                    *,
                    name: str
                    ) -> bool:
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
    def update_kwargs_by_name(cls,
                              *,
                              name: str,
                              kwargs: Dict[str, Any]
                              ) -> 'cls':
        """
        根据name来查询记录，并且更新一些字段
        如果不存在，则抛出异常
        建议前置判断存在的函数
        """
        kwargs = remove_none_and_cls_kwargs(kwargs=kwargs)

        record = cls.get_by_name(name=name)
        if record is None:
            raise ValueError(f'name: {name} 对应的记录不存在！')
        for k, v in kwargs.items():
            setattr(record, k, v)
        session.commit()
        return record

    @classmethod
    def update_name_by_name(cls,
                            *,
                            old_name: str,
                            new_name: str
                            ) -> 'cls':
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
    def update_name_by_id(cls,
                          *,
                          _id: str,
                          new_name: str
                          ) -> 'cls':
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
    def get_by_name(cls,
                    *,
                    name: str
                    ) -> 'cls':
        """
        根据name进行查询，返回第一条记录
        如果存在则返回true，如果不存在
        """
        record = cls.query_one_by_name(name=name)
        return record

    @classmethod
    def is_exists_by_name(cls,
                          *,
                          name: str
                          ) -> 'cls':
        """
        根据name进行查询
        存在返回true，不存在返回false
        """
        record = cls.query_one_by_name(name=name)
        return record is not None

    @classmethod
    def _add_or_update_by_name(cls,
                               *,
                               kwargs: Dict[str, Any],
                               ) -> 'cls':
        """
        返回新增或者更新后的记录。
        如果update的时候，name不存在，则抛出异常
        """
        name = kwargs['name']
        remove_none_and_cls_kwargs(kwargs=kwargs)
        if cls.is_exists_by_name(name=name):
            kwargs.pop("name")
            return cls.update_kwargs_by_name(name=name, kwargs=kwargs)
        else:
            return cls.add_with_kwargs(kwargs=kwargs)

    # 虚类
    @classmethod
    @abstractmethod
    def add_or_update_by_id(cls,
                            *,
                            name: str,
                            kwargs: Dict[str, Any]
                            ) -> 'cls':
        """
        返回新增或者更新后的记录。
        """
        ...

    # 虚类
    @classmethod
    @abstractmethod
    def add_or_update_by_name(cls,
                              *,
                              name: str,
                              kwargs: Dict[str, Any]
                              ) -> 'cls':
        """
        强制继承自他的类，必须实现这个方法，如果不实现，也要声明为抽象方法；
        """
        ...
