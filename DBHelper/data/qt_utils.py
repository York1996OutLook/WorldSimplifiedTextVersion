from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, \
    QPushButton, QListWidget, QMessageBox, QFrame, QComboBox
from PyQt5.QtCore import pyqtSignal, pyqtBoundSignal, QMetaObject
import PyQt5.QtGui as QtGui

class TableItems:
    """
            self.current_data_table_combo_box.addItem("技能")
        self.current_data_table_combo_box.addItem("状态")
        self.current_data_table_combo_box.addItem("5大基础属性")
    """
    skill="技能"
    status="状态"
    base_property='5大基础属性'


class MyLineText(QLineEdit):
    focus: pyqtBoundSignal = pyqtSignal(int, str)
    text_change: pyqtBoundSignal = pyqtSignal(int, str)

    def __init__(self, index: int, parent: QWidget = None):
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


class MyButton(QPushButton):
    def __init__(self,*,text:str):
        super().__init__()
        self.setText(text)
    def disconnect_all(self) -> bool:
        try:
            self.disconnect()
        except :
            return


class MyFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.style_sheet = 'border: 1px solid black;'
        self.setStyleSheet(self.style_sheet)


class MyLabel(QLabel):
    def __init__(self, label_text: str = ""):
        super().__init__()
        self.setText(label_text)
        self.style_sheet = 'border: 1px solid black;'
        self.setStyleSheet(self.style_sheet)


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


class EditType:
    combo_box = 1
    short_text = 2
    long_text = 3


def set_geo(*,
            cur_widget: QWidget,
            parent_widget: QWidget,
            x1: int,
            y1: int,
            width: int,
            height: int):
    cur_widget.setParent(parent_widget)
    cur_widget.setGeometry(x1, y1, width, height)
