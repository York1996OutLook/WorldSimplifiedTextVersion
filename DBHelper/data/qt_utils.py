# 2023年4月21日 QLineEdit支持setText(None)

from collections import defaultdict
import inspect
from typing import List, Dict, Any

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, \
    QPushButton, QListWidget, QMessageBox, QFrame, QComboBox, QDateTimeEdit, QTextEdit, QScrollArea
from PyQt5.QtCore import pyqtSignal, pyqtBoundSignal, QMetaObject
import PyQt5.QtGui as QtGui

from DBHelper.tables.base_table import Basic
from DBHelper.db import *
from Enums import DataType, AdditionSourceType, Item, StuffType


class TableItemList:
    def __init__(self):
        TableItem.item_list = self

        self.items: [TableItem] = []
        self.name_dict = defaultdict(None)
        self.index_dict = defaultdict(None)
        self.counter: int = 0

    def clear(self):
        self.items: [TableItem] = []

    def get_items(self) -> ["TableItem"]:
        return self.items

    def get_by_index(self, *, index: int) -> "TableItem":
        return self.index_dict[index]

    def get_by_name(self, *, name: str) -> "TableItem":
        return self.name_dict[name]


class TableItem:
    item_list: TableItemList = None

    def __init__(self, *,
                 table_class=None,  # orm class 类型
                 comment: str = '',
                 index: int = None,
                 addition_source_type: Item = None,
                 bind_stuff_type: Item = None,
                 editable: bool = True,
                 is_entity: bool = None,
                 sub_type_field: str = None,
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
        self.is_entity = is_entity
        self.bind_stuff_type = bind_stuff_type
        self.sub_type_field = sub_type_field    # 第一级类型划分

        self.sub_type_field_column=None
        self.sub_type_field_column_bind_type=None
        self.sub_type_index=None

        self.item_list.items.append(self)
        if self.name in self.item_list.name_dict:
            raise ValueError(f"name:{self.name} is already exists!")
        if self.name in self.item_list.index_dict:
            raise ValueError(f"index:{self.index} is already exists!")

        self.item_list.name_dict[self.name] = self
        self.item_list.index_dict[self.index] = self

    def __repr__(self):
        return f'TableItem( table_class:{self.table_class}  ' \
               f'{self.index}: {self.name},addition_source_type:{self.addition_source_type}' \
               f'editable:{self.editable}, {self.comment})'


class TableItems:
    item_list = TableItemList()
    achievement = TableItem(table_class=Achievement,
                            addition_source_type=AdditionSourceType.ACHIEVEMENT_TITLE,
                            sub_type_field="achievement_type")
    skill = TableItem(table_class=SkillBook,
                      addition_source_type=AdditionSourceType.SKILL_BOOK)
    battle_status = TableItem(table_class=BattleStatus,
                              addition_source_type=AdditionSourceType.STATUS)
    achievement_title_book = TableItem(table_class=AchievementTitleBook)
    monster = TableItem(table_class=Monster,
                        addition_source_type=AdditionSourceType.MONSTER,
                        bind_stuff_type=StuffType.MONSTER,
                        )
    potion = TableItem(table_class=Potion,
                       addition_source_type=AdditionSourceType.POTION)
    player_or_monster_skill_setting = TableItem(table_class=PlayerOrMonsterSkillSetting)

    setting = TableItem(table_class=Setting)
    dust = TableItem(table_class=Dust)
    gem = TableItem(table_class=Gem)
    box = TableItem(table_class=Box, bind_stuff_type=StuffType.BOX)
    exp_book = TableItem(table_class=ExpBook)
    holiday = TableItem(table_class=Holiday)
    equipment = TableItem(table_class=Equipment,
                          addition_source_type=AdditionSourceType.EQUIPMENT_PROTOTYPE,
                          bind_stuff_type=StuffType.EQUIPMENT)

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

    player_achievement_record = TableItem(table_class=PlayerAchievementRecord, editable=False)
    player_use_book_record = TableItem(table_class=PlayerUseStuffRecord, editable=False)
    player_stuff_record = TableItem(table_class=PlayerStuffRecord, editable=False)
    player_skill_record = TableItem(table_class=PlayerSkillRecord, editable=False)
    player_potion_record = TableItem(table_class=PlayerPotionRecord, editable=False)
    player_lottery_record = TableItem(table_class=PlayerLotteryRecord, editable=False)
    player_mail_record = TableItem(table_class=PlayerMailRecord, editable=False)
    equipment_gem_record = TableItem(table_class=EquipmentGemRecord, editable=False)
    equipment_star_record = TableItem(table_class=EquipmentStarRecord, editable=False)

    player = TableItem(table_class=Player,
                       addition_source_type=AdditionSourceType.PLAYER,
                       editable=False)
    sell_store = TableItem(table_class=PlayerSellStoreRecord, editable=False)
    pk_rank = TableItem(table_class=PK_Rank,
                        addition_source_type=AdditionSourceType.PK_RANK,
                        editable=False)
    player_battle_record = TableItem(table_class=PlayerBattleRecord, editable=False)
    # base_property = '5大基础属性'  # 稍后再决定如何实现非单独定义表格数据的实现

    default = achievement


class BaseWidget(QWidget):
    def __init__(self):
        super(BaseWidget, self).__init__()
        screen_resolution = QtWidgets.QDesktopWidget().screenGeometry()
        width = screen_resolution.width()
        height = screen_resolution.height()
        if width > 1920 and height > 1080:
            font_size = 10  # 4K及以上屏幕
        elif width > 1920 or height > 1080:
            font_size = 8  # 1080p及以上屏幕
        else:
            font_size = 10  # 普通屏幕
        font = QtGui.QFont()
        font.setPointSize(font_size)
        self.setFont(font)

    def disconnect_all(self) -> bool:
        try:
            self.disconnect()
        except:
            return False

    def right(self):
        return self.geometry().right()

    def left(self):
        return self.geometry().left()

    def top(self):
        return self.geometry().top()

    def bottom(self):
        return self.geometry().bottom()

class MyLineText(QLineEdit, BaseWidget):
    focus: pyqtBoundSignal = pyqtSignal(int, int, str)
    text_change: pyqtBoundSignal = pyqtSignal(int, int, str)

    def __init__(self, *, main_index: int = 0, sub_index=0, text: str = ""):
        super().__init__()
        self.main_index = main_index
        self.sub_index = sub_index
        self.textChanged.connect(self.text_change_event)
        self.style_sheet_focused = 'border: 2px solid blue;'
        self.style_sheet_default = 'border: 1px solid black;'

        if text:
            self.setText(text)

    def text_change_event(self, ev):
        self.setStyleSheet(self.style_sheet_focused)
        self.text_change.emit(self.main_index, self.sub_index, self.text())

    def focusInEvent(self, a0: QtGui.QFocusEvent) -> None:
        self.setStyleSheet(self.style_sheet_focused)
        self.focus.emit(self.main_index, self.sub_index, self.text())

    def focusOutEvent(self, a0: QtGui.QFocusEvent) -> None:
        self.setStyleSheet(self.style_sheet_default)

    def set_text(self, *, text: str or int or bool or None) -> None:
        if text is None:
            print("None->空字符串")
            text = ""
        if type(text) == int:
            text = str(text)
        if type(text) == bool:
            text = str(text)
        self.setText(text)

    def text(self) -> str:
        return super(MyLineText, self).text().strip()


class MyMultiLineText(QTextEdit, BaseWidget):
    focus: pyqtBoundSignal = pyqtSignal(int, str)
    text_change: pyqtBoundSignal = pyqtSignal(int, str)

    def __init__(self, *, index: int = -1):
        super().__init__()
        self.index = index
        self.textChanged.connect(self.text_change_event)
        self.style_sheet_focused = 'border: 2px solid blue;'
        self.style_sheet_default = 'border: 1px solid black;'

    def text_change_event(self):
        self.setStyleSheet(self.style_sheet_focused)
        self.text_change.emit(self.index, self.text())

    def focusInEvent(self, a0: QtGui.QFocusEvent) -> None:
        self.setStyleSheet(self.style_sheet_focused)
        self.focus.emit(self.index, self.text())

    def focusOutEvent(self, a0: QtGui.QFocusEvent) -> None:
        self.setStyleSheet(self.style_sheet_default)

    def set_text(self, *, text: str or int or bool or None) -> None:
        if text is None:
            print("None->空字符串")
            text = ""
        if type(text) == int:
            text = str(text)
        if type(text) == bool:
            text = str(text)
        self.setText(text)

    def text(self) -> str:
        return super(MyMultiLineText, self).toPlainText().strip()


class MyButton(QPushButton, BaseWidget):
    def __init__(self, *, text: str):
        super().__init__()
        self.setText(text)


class MyAddSubButton(QPushButton, BaseWidget):
    push: pyqtBoundSignal = pyqtSignal(int, int)

    def __init__(self, *, text: str, main_index: int, sub_index: int = 0):
        super().__init__()
        self.setText(text)
        self.main_index = main_index
        self.sub_index = sub_index

        self.clicked.connect(self.click_button)

    def click_button(self) -> None:
        self.push.emit(self.main_index, self.sub_index + 1)


class MyListBox(QListWidget, BaseWidget):
    def __init__(self):
        super().__init__()

    def text(self):
        if not self.currentItem():
            return ""
        return self.currentItem().text().strip()


class MyFrame(QFrame, BaseWidget):
    def __init__(self):
        super().__init__()
        self.style_sheet = 'border: 1px solid black;'
        self.setStyleSheet(self.style_sheet)


class MyScrollArea(QScrollArea, BaseWidget):
    def __init__(self):
        super(MyScrollArea, self).__init__()
        self.style_sheet = 'border: 1px solid black;'
        self.setStyleSheet(self.style_sheet)


class MyLabel(QLabel, BaseWidget):
    def __init__(self, *, label_text: str = ""):
        super(MyLabel, self).__init__()
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


class MyComboBox(QComboBox, BaseWidget):
    def __init__(self):
        super(MyComboBox, self).__init__()

    def set_text(self, *, text: str or bool):
        if type(text) == bool:
            text = str(text)
        self.setCurrentText(text)

    def text(self):
        return self.currentText().strip()


class MyDateTimeBox(QDateTimeEdit, BaseWidget):
    def __init__(self):
        super(MyDateTimeBox, self).__init__()


class EditWidgetType:
    combo_box = 1
    short_text = 2
    long_text = 3
    bool_combo_box = 4
    date_time_box = 5
    multiline_text_box = 6


class ColumnEdit:
    def __init__(self, *,
                 data_type: DataType,
                 key: str,
                 cn: str,
                 edit_widget_type: EditWidgetType,
                 bind_type=None,  # enums里面的枚举类型。包含item list 和 default
                 bind_table: Basic = None,  #
                 choices: List[str] = None,
                 editable: bool = True,
                 default: Any = None):
        if bind_type is not None and bind_table is not None:
            raise ValueError("table 和 type只能指定一个")
        self.data_type = data_type
        self.key = key
        self.cn = cn
        self.edit_widget_type = edit_widget_type
        self.bind_type = bind_type  # bind_type 和 bind_type只能有一个
        self.bind_table = bind_table
        self.choices = choices
        self.editable = editable

        self.edit_label: MyLabel = None
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


class PropertyWidgets:
    """
    和属性相关的若干控件
    """

    def __init__(self,
                 *,
                 add_sub_property_button: MyButton,
                 index_label: MyLabel,
                 name_input_text: MyLineText,

                 name_label: MyLabel,
                 min_value_label: MyLabel,
                 min_value_text: MyLineText,
                 max_value_label: MyLabel,
                 max_value_text: MyLineText,

                 temp_value_label: MyLabel,
                 temp_value_text: MyLineText,

                 cur_value_label: MyLabel,
                 cur_value_text: MyLineText,
                 ):
        self.add_sub_property_button = add_sub_property_button
        self.index_label = index_label
        self.name_input_text = name_input_text

        self.name_label = name_label

        self.min_value_label = min_value_label
        self.min_value_text = min_value_text
        self.max_value_label = max_value_label
        self.max_value_text = max_value_text

        self.temp_value_label = temp_value_label
        self.temp_value_text = temp_value_text

        self.cur_value_label = cur_value_label
        self.cur_value_text = cur_value_text

        self.all_widgets = [
            add_sub_property_button,
            index_label,

            name_input_text,
            name_label,

            min_value_label,
            min_value_text,
            max_value_label,
            max_value_text,

            temp_value_label,
            temp_value_text,

            cur_value_label,
            cur_value_text,
        ]
        self.should_clear_widgets = [
            name_input_text,

            min_value_text,
            max_value_text,
            temp_value_text,
            cur_value_text,
        ]


class DropStuffWidgets:
    """
    和属性相关的若干控件
    """

    def __init__(self,
                 *,
                 index_label: MyLabel,
                 name_input_text: MyLineText,

                 stuff_type_label: MyLabel,
                 stuff_type_combo_box: MyComboBox,

                 name_label: MyLabel,
                 prob_label: MyLabel,
                 prob_value_text: MyLineText):
        self.index_label = index_label
        self.name_input_text = name_input_text

        self.stuff_type_label = stuff_type_label
        self.stuff_type_combo_box = stuff_type_combo_box

        self.name_label = name_label
        self.prob_label = prob_label
        self.prob_value_text = prob_value_text

        self.all_widgets = [
            index_label,
            name_input_text,
            name_input_text,
            stuff_type_label,
            stuff_type_combo_box,
            name_label,
            prob_label,
            prob_value_text,
        ]
        self.should_clear_widgets = [
            name_input_text,
            stuff_type_label,
            prob_value_text,
            stuff_type_combo_box,
        ]


def set_geo(*,
            cur_widget: QWidget,
            parent_widget: QWidget,
            x1: int,
            y1: int,
            width: int,
            height: int):
    cur_widget.setParent(parent_widget)
    cur_widget.setGeometry(x1, y1, width, height)
