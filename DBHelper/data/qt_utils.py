# 2023年4月21日 QLineEdit支持setText(None)

from collections import defaultdict
import inspect
from typing import List, Dict

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, \
    QPushButton, QListWidget, QMessageBox, QFrame, QComboBox
from PyQt5.QtCore import pyqtSignal, pyqtBoundSignal, QMetaObject
import PyQt5.QtGui as QtGui

from DBHelper.tables.base_table import Basic
from DBHelper.db import *
from Enums import DataType, AdditionSourceType,Item


class TableItemList:
    def __init__(self):
        TableItem.item_list = self

        self.items: [TableItem] = []
        self.name_index_dict = defaultdict(None)
        self.index_name_dict = defaultdict(None)
        self.counter:int = 0

    def clear(self):
        self.items: [TableItem] = []

    def get_items(self) -> ["TableItem"]:
        return self.items

    def get_by_index(self, *, index: int) -> "TableItem":
        return self.index_name_dict[index]

    def get_by_name(self, *, name: str) -> "TableItem":
        return self.name_index_dict[name]


class TableItem:
    item_list:TableItemList = None

    def __init__(self, *,
                 table_class=None,
                 comment: str = '',
                 index: int = None,
                 addition_source_type: Item= None,
                 editable: bool = True
                 ):
        if index:
            self.index = index
        else:
            self.index = len(self.item_list.items) + 1

        self.table_class = table_class
        self.name = table_class.__cn__
        self.comment = comment
        self.addition_source_type = addition_source_type
        self.editable = editable

        self.item_list.items.append(self)
        self.item_list.name_index_dict[self.name] = self
        self.item_list.index_name_dict[self.index] = self

    def __repr__(self):
        return f'TableItem( table_class:{self.table_class}  ' \
               f'{self.index}: {self.name},addition_source_type:{self.addition_source_type}' \
               f'editable:{self.editable}, {self.comment})'


class TableItems:
    item_list = TableItemList()
    achievement = TableItem(table_class=Achievement, addition_source_type=AdditionSourceType.ACHIEVEMENT_TITLE)
    skill = TableItem(table_class=SkillBook, addition_source_type=AdditionSourceType.SKILL_BOOK)
    battle_status = TableItem(table_class=BattleStatus, addition_source_type=AdditionSourceType.STATUS)
    achievement_title_book = TableItem(table_class=AchievementTitleBook)
    monster = TableItem(table_class=Monster, addition_source_type=AdditionSourceType.MONSTER)
    potion = TableItem(table_class=Potion, addition_source_type=AdditionSourceType.POTION)
    player_or_monster_skill_setting = TableItem(table_class=PlayerOrMonsterSkillSetting)

    setting = TableItem(table_class=Setting)
    dust = TableItem(table_class=Dust)
    gem = TableItem(table_class=Gem)
    box = TableItem(table_class=Box)
    exp_book = TableItem(table_class=ExpBook)
    holiday = TableItem(table_class=Holiday)
    equipment = TableItem(table_class=Equipment)

    equipment_quality_dust_num = TableItem(table_class=EquipmentQualityDustNum)
    identify_book = TableItem(table_class=IdentifyBook)
    monster_type_show_time = TableItem(table_class=MonsterShowUpRecord, )
    raise_star_book = TableItem(table_class=RaiseStarBook)
    raise_star_prob = TableItem(table_class=RaiseStarProb)
    skill_cost_point = TableItem(table_class=SkillCostPoint)
    level_exp = TableItem(table_class=PlayerLevelExpSkillPoint)
    skill_slot = TableItem(table_class=SkillSlot)
    tips = TableItem(table_class=Tips)
    world_hero_medal = TableItem(table_class=WorldHeroMedal)

    player_use_book_record = TableItem(table_class=PlayerUseStuffRecord, editable=False)
    player_stuff_record = TableItem(table_class=PlayerStuffRecord, editable=False)
    player_skill_record = TableItem(table_class=PlayerSkillRecord, editable=False)
    player_potion_record = TableItem(table_class=PlayerPotionRecord, editable=False)
    player_lottery_record = TableItem(table_class=PlayerLotteryRecord, editable=False)
    player_mail_record = TableItem(table_class=PlayerMailRecord, editable=False)
    equipment_gem_record = TableItem(table_class=EquipmentGemRecord, editable=False)
    equipment_star_record = TableItem(table_class=EquipmentStarRecord, editable=False)

    player = TableItem(table_class=Player, addition_source_type=AdditionSourceType.PLAYER, editable=False)
    sell_store = TableItem(table_class=PlayerSellStoreRecord, editable=False)
    pk_rank = TableItem(table_class=PK_Rank, editable=False)
    player_battle_record = TableItem(table_class=PlayerBattleRecord, editable=False)
    # base_property = '5大基础属性'  # 稍后再决定如何实现非单独定义表格数据的实现

    default = achievement


class MyLineText(QLineEdit):
    focus: pyqtBoundSignal = pyqtSignal(int, str)
    text_change: pyqtBoundSignal = pyqtSignal(int, str)

    def __init__(self, index: int = -1, parent: QWidget = None):
        super().__init__(parent)
        self.index = index
        self.textChanged.connect(self.text_change_event)
        self.style_sheet_focused = 'border: 2px solid blue;'
        self.style_sheet_default = 'border: 1px solid black;'

    def text_change_event(self, ev):
        self.setStyleSheet(self.style_sheet_focused)
        self.text_change.emit(self.index, self.text())

    def focusInEvent(self, a0: QtGui.QFocusEvent) -> None:
        self.setStyleSheet(self.style_sheet_focused)
        self.focus.emit(self.index, self.text())

    def focusOutEvent(self, a0: QtGui.QFocusEvent) -> None:
        self.setStyleSheet(self.style_sheet_default)

    def set_text(self, *, text: str or int or None) -> None:
        if text is None:
            print("None->空字符串")
            text = ""
        if type(text) == int:
            text = str(text)
        self.setText(text)


class MyButton(QPushButton):
    def __init__(self, *, text: str):
        super().__init__()
        self.setText(text)

    def disconnect_all(self) -> bool:
        try:
            self.disconnect()
        except:
            return


class MyListBox(QListWidget):
    def __init__(self):
        super().__init__()

    def disconnect_all(self) -> bool:
        try:
            self.disconnect()
        except:
            return


class MyFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.style_sheet = 'border: 1px solid black;'
        self.setStyleSheet(self.style_sheet)


class MyLabel(QLabel):
    def __init__(self, label_text: str = ""):
        super().__init__()
        self.set_text(text=label_text)
        self.style_sheet = 'border: 1px solid black;'
        self.setStyleSheet(self.style_sheet)

    def set_text(self, *, text: str or int or None) -> None:
        if text is None:
            print("None->空字符串")
            text = ""
        if type(text) == int:
            text = str(text)
        self.setText(text)


class EditWidgetType:
    combo_box = 1
    short_text = 2
    long_text = 3
    bool_combo_box = 4


class DataEdit:
    def __init__(self, *,
                 data_type: DataType,
                 key: str,
                 cn: str,
                 edit_widget_type: EditWidgetType,
                 choices=None,
                 editable: bool = True,
                 default=None):
        self.data_type = data_type
        self.key = key
        self.cn = cn
        self.edit_widget_type = edit_widget_type
        self.choices = choices
        self.editable = editable

        self.edit_widget: MyLineText or MyComboBox or MyListBox = None

        self.default = default


class StatuesWidgets:
    """
    和属性相关的若干控件
    """

    def __init__(self,
                 *,
                 statues_index_label: MyLabel,
                 statues_name_text: MyLineText,
                 statues_name_label: MyLabel, ):
        self.statues_index_label = statues_index_label
        self.statues_name_text = statues_name_text
        self.statues_name_label = statues_name_label


class MyComboBox(QComboBox):
    def __init__(self):
        super(MyComboBox, self).__init__()

    def set_text(self, *, text: str):
        self.setCurrentText(text)

    def text(self):
        return self.currentText()


class PropertyWidgets:
    """
    和属性相关的若干控件
    """

    def __init__(self,
                 *,
                 index_label: MyLabel,
                 name_text: MyLineText,

                 # target_label: MyLabel,
                 # target_combo_box: QComboBox,
                 availability_combo_box:MyComboBox,
                 name_label: MyLabel,
                 value_text: MyLineText):
        self.index_label = index_label
        self.name_text = name_text

        # self.target_label = target_label
        # self.target_combo_box = target_combo_box

        self.name_label = name_label
        self.value_text = value_text

        self.availability_combo_box=availability_combo_box
        print(1)


def set_geo(*,
            cur_widget: QWidget,
            parent_widget: QWidget,
            x1: int,
            y1: int,
            width: int,
            height: int):
    cur_widget.setParent(parent_widget)
    cur_widget.setGeometry(x1, y1, width, height)
