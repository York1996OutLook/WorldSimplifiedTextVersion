from collections import defaultdict


class Item:
    _tags = dict()
    _items = []
    _name_index_dict = defaultdict(dict)
    _index_name_dict = defaultdict(dict)

    def __init__(self, *, tag: str, name: str, comment: str = ''):
        self.tag = tag
        if not self.tag in Item._tags.keys():
            Item._tags.update({self.tag: 1})
        else:
            Item._tags[self.tag] += 1
        self.index = Item._tags[self.tag]
        self.name = name
        self.comment = comment

        Item._items.append(self)

        Item._name_index_dict[self.tag].update({self.name: self.index})
        Item._index_name_dict[self.tag].update({self.index: self.name})

    @classmethod
    def clear(cls):
        cls._items = []
        cls._counter = 0

    @classmethod
    def get_items(cls):
        return cls._items

    @classmethod
    def get_name_by_index(cls, *, tag: str, index: int):
        if index in Item._index_name_dict[tag]:
            return Item._index_name_dict[tag][index]
        else:
            raise KeyError('no such index')

    @classmethod
    def get_index_by_name(cls, *, tag: str, name: str):
        if name in Item._name_index_dict[tag]:
            return Item._name_index_dict[tag][name]
        else:
            raise KeyError('no such name')

    def __repr__(self):
        return f'Item({self.index}: {self.name}, {self.comment})'


class SkillTarget:
    name = "作用目标"

    SELF = Item(tag='skill', name='自身', comment='自身')
    ENEMY = Item(tag='skill', name="敌人", comment="敌人")

    DATA = Item
    default = SELF


class StatusType:
    name = '状态类型'

    PASSIVE = Item(tag='status', name='减益', comment='减益')
    POSITIVE = Item(tag='status', name="增益", comment="增益")
    NEUTRAL = Item(tag='status', name="中立", comment="中立")

    DATA = Item
    default = PASSIVE


a = SkillTarget
b = StatusType

print(b.DATA.get_name_by_index(tag='skill', index=1))

print(a.DATA.get_index_by_name(tag='status', name='中立'))

print(Item._items)
