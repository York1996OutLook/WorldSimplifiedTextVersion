# 2023年4月21日 QLineEdit支持setText(None)

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, \
    QPushButton, QListWidget, QMessageBox, QFrame, QComboBox
from PyQt5.QtCore import pyqtSignal, pyqtBoundSignal, QMetaObject
import PyQt5.QtGui as QtGui

from Enums import StatusType


class TableItems:
    setting = '设置'  # 计划做成可以滚动的浏览框

    skill = "技能"
    status = "状态"
    base_property = '5大基础属性'
    achievement = '成就'
    gem = '宝石'
    box = '盒子'
    exp_book = '经验书'
    holiday = '节日'
    equipment = '装备' # 可能会做成两个选择框的形式。自动出现一个combo_box
    identify_book = '鉴定卷轴'
    monster = '怪物'  # 包含技能设置
    monster_type_show_time = '选择怪物类型选择出现时间'
    potion = '药水'
    raise_star_book = '升星卷轴'
    raise_star_prob = '升星成功概率'
    skill_cost_point = '学习技能消耗技能点'
    level_exp = '升级所需经验'



    player = '玩家'   # 建议不修改，仅仅查看而已
    sell_store = '交易所'   # 建议不修改，仅仅查看而已




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

    def set_text(self, a0: str or int or None) -> None:
        if a0 is None:
            print("None->空字符串")
            a0 = ""
        if type(a0) == int:
            a0 = str(a0)
        self.setText(a0)


class MyButton(QPushButton):
    def __init__(self, *, text: str):
        super().__init__()
        self.setText(text)

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
        self.set_text(label_text)
        self.style_sheet = 'border: 1px solid black;'
        self.setStyleSheet(self.style_sheet)

    def set_text(self, a0: str or int or None) -> None:
        if a0 is None:
            print("None->空字符串")
            a0 = ""
        if type(a0) == int:
            a0 = str(a0)
        self.setText(a0)


class EditType:
    combo_box = 1
    short_text = 2
    long_text = 3
    bool_combo_box = 4



class DataEditType:
    def __init__(self, *, key: str, label: str, edit_widget: EditType, choices=None, editable: bool = True,default=None):
        self.key = key
        self.label = label
        self.edit_widget = edit_widget
        self.choices = choices
        self.editable = editable

        self.default=default


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
                 index_label: MyLabel,
                 name_text: MyLineText,

                 target_label: MyLabel,
                 target_combo_box: QComboBox,

                 name_label: MyLabel,
                 value_text: MyLineText):
        self.index_label = index_label
        self.name_text = name_text

        self.target_label = target_label
        self.target_combo_box = target_combo_box

        self.name_label = name_label
        self.value_text = value_text
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
