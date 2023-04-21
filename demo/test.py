class ItemList:
    def __init__(self):
        self.items = []
        self.name_index_dict = dict()
        self.index_name_dict = dict()
        self.counter = 0

    def clear(self):
        self.items = []

    def get_items(self):
        return self.items

    def get_name_by_index(self, *, index: int):
        return self.index_name_dict[index]

    def get_index_by_name(self, *, name: str):
        return self.name_index_dict[name]


class Item:
    def __init__(self, *, name: str, comment: str = '', item_list: ItemList):
        self.index = len(item_list.items) + 1
        self.name = name
        self.comment = comment
        item_list.items.append(self)
        item_list.name_index_dict[self.name] = self.index
        item_list.index_name_dict[self.index ] = self.name

    def __repr__(self):
        return f'Item({self.index}: {self.name}, {self.comment})'


class SkillTarget:
    name = "作用目标"
    item_list = ItemList()

    SELF = Item(name='自身', comment='自身', item_list=item_list)
    ENEMY = Item(name="敌人", comment="敌人", item_list=item_list)

    default = SELF


class StatusType:
    name = '状态类型'
    item_list = ItemList()

    PASSIVE = Item(name='减益', comment='减益', item_list=item_list)
    POSITIVE = Item(name="增益", comment="增益", item_list=item_list)
    NEUTRAL = Item(name="中立", comment="中立", item_list=item_list)

    default = PASSIVE


a = SkillTarget
b = StatusType
print(b.item_list.get_name_by_index(index=1))
print(a.item_list.get_name_by_index(index=1))

#
# a = Item(name='a')
# b = Item(name='b')
# c = Item(name='c')
#
# print(a.index)
# print(b.index)
# print(c.index)
#
# print(Item.get_name_by_index(index=1))
# print(Item.get_index_by_name(name='b'))
#
# print(c)
