class ItemList:
    def __init__(self):

        Item.item_list=self

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
    item_list = None

    def __init__(self, *, name: str, comment: str = '', ):
        self.index = len(self.item_list.items) + 1
        self.name = name
        self.comment = comment

        self.item_list.items.append(self)
        self.item_list.name_index_dict[self.name] = self.index
        self.item_list.index_name_dict[self.index] = self.name

    def __repr__(self):
        return f'Item({self.index}: {self.name}, {self.comment})'



class SkillTarget:
    name = "作用目标"
    item_list = ItemList()

    SELF = Item(name='自身', comment='自身')
    ENEMY =Item(name="敌人", comment="敌人")

    default = SELF


class StatusType:
    name = '状态类型'
    item_list = ItemList()

    PASSIVE = Item(name='减益', comment='减益')
    POSITIVE =Item(name="增益", comment="增益")

    default = PASSIVE


a = SkillTarget
b = StatusType
print(b.item_list.get_name_by_index(index=1))
print(a.item_list.get_name_by_index(index=1))