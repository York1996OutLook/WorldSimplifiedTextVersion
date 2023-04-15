from Enums import AdditionSourceType, property_cn_type_dict, property_type_cn_dict

import sys
from collections import defaultdict
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, \
    QPushButton, QListWidget, QMessageBox, QFrame, QComboBox
import numpy as np
from PyQt5.QtCore import pyqtSignal, pyqtBoundSignal
import PyQt5.QtGui as QtGui

from DBHelper.db import *


class EditType:
    combo_box = 1
    short_text = 2
    long_text = 3


class MyLineText(QLineEdit):
    focus: pyqtBoundSignal = pyqtSignal(int, str)
    text_change: pyqtBoundSignal = pyqtSignal(int, str)

    def __init__(self, index: int, parent: QWidget = None):
        super().__init__(parent)
        self.index = index
        self.textChanged.connect(self.text_change_event)

    def text_change_event(self, ev):
        self.text_change.emit(self.index, self.text())

    def focusInEvent(self, a0: QtGui.QFocusEvent) -> None:
        self.focus.emit(self.index, self.text())


class PropertyWidgets:
    """
    和属性相关的若干控件
    """

    def __init__(self,
                 *,
                 property_index_label: QLabel,
                 property_name_text: MyLineText,
                 property_name_label: QLabel,
                 property_value_text: MyLineText):
        self.property_index_label = property_index_label
        self.property_name_text = property_name_text
        self.property_name_label = property_name_label
        self.property_value_text = property_value_text
        print(1)


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.left_right_region_height = 500
        self.left_region_width = 200
        self.bottom_region_height = 70
        self.item_height = 40

        self.label_width = 50  # 属性1，属性2，
        self.short_text_width = 100  # 具体属性名字输入
        self.long_text_width = 300  # 具体属性名字输入
        self.long_label_width = 100  # 具体属性名字展示

        self.right_top_region_height = 200

        self.button_width = 100
        self.button_top_margin = 20

        self.property_list_width = 120
        self.interval = 5

        #
        self.style_sheet = 'border: 1px solid black;'
        # 区域划分
        self.left_region = QFrame()
        self.right_region = QFrame()
        self.right_top_region = QFrame()
        self.right_bottom_region = QFrame()
        self.bottom_region = QFrame()

        # 技能列表区域
        self.skillsListWidget = QListWidget()

        self.properties_widgets_list = []  # 包含property_index_label,property_name_text,property_value_text,
        self.all_property_list_widget = QListWidget()

        # 设置区域
        self.setting_list = [
            # 数据库中对应的属性值，属性标签的名称，属性标签的编辑方式，可选项
            ("skill_name", "技能名称", EditType.short_text, ""),
            ("level", "等级", EditType.combo_box, ("9",)),
            ("in_skill_store", "在商店中", EditType.combo_box, ("True", "False")),
            ("is_positive", "是否为主动技能", EditType.combo_box, ("True", "False")),
            ("effect_expression", "技能说明", EditType.long_text, ""),
        ]
        self.setting_widget_dict = dict()

        self.saveButton = QPushButton('保存')

        self.new_skill_label = QLabel()
        self.new_skill_line_text = QLineEdit()
        self.add_skill_button = QPushButton("新增")

        self.skills = skill.get_all()
        self.initUI()
        self.current_properties_index = 0

    @staticmethod
    def set_geo(*, cur_widget: QWidget, parent_widget: QWidget, x1: int, y1: int, width: int, height: int):
        cur_widget.setParent(parent_widget)
        cur_widget.setGeometry(x1, y1, width, height)

    def initUI(self):
        right_region_width = self.property_list_width + self.label_width + \
                             self.short_text_width + self.long_label_width + self.label_width + self.interval * 6

        left_right_region_width = self.left_region_width + right_region_width

        self.setWindowTitle('属性表:')
        self.setGeometry(0,
                         0,
                         left_right_region_width,
                         self.left_right_region_height + self.bottom_region_height)

        # 左
        self.left_region.setStyleSheet(self.style_sheet)
        self.set_geo(cur_widget=self.left_region,
                     parent_widget=self,
                     x1=0,
                     y1=0,
                     width=self.left_region_width,
                     height=self.left_right_region_height)
        # 右边
        self.right_region.setStyleSheet(self.style_sheet)
        self.set_geo(cur_widget=self.right_region,
                     parent_widget=self,
                     x1=self.left_region_width,
                     y1=0,
                     width=right_region_width, height=self.left_right_region_height)

        # 右上
        self.right_top_region.setStyleSheet(self.style_sheet)
        self.set_geo(cur_widget=self.right_top_region,
                     parent_widget=self.right_region,
                     x1=0,
                     y1=0,
                     width=right_region_width, height=self.right_top_region_height)
        # 右下
        self.right_bottom_region.setStyleSheet(self.style_sheet)
        self.set_geo(cur_widget=self.right_bottom_region,
                     parent_widget=self.right_region,
                     x1=0,
                     y1=self.right_top_region_height,
                     width=right_region_width, height=self.left_right_region_height - self.right_top_region_height)
        # 下方
        self.set_geo(cur_widget=self.bottom_region,
                     parent_widget=self,
                     x1=0,
                     y1=self.left_right_region_height,
                     width=left_right_region_width,
                     height=self.bottom_region_height,
                     )

        self.init_skill_list_widgets()
        self.init_property_widgets()
        self.init_property_list()
        self.init_bottom_widgets()
        self.init_skill_setting_ui()

    def init_skill_list_widgets(self):
        # 创建显示技能的列表
        self.set_geo(cur_widget=self.skillsListWidget,
                     parent_widget=self.left_region,
                     x1=0,
                     y1=0,
                     width=self.left_region_width,
                     height=self.left_right_region_height)

        self.skillsListWidget.itemClicked.connect(self.handle_skill_changed)
        self.skillsListWidget.setFixedWidth(self.left_region_width)
        self.show_all_skills()

    def init_property_widgets(self):
        # 创建显示属性的文本框和按钮
        for index in range(4):
            property_index_label = QLabel(f'属性：{index + 1}')
            property_name_text = MyLineText(index)
            # -------------------------------------
            property_name_label = QLabel()
            property_value_text = MyLineText(index)

            # 设置样式：
            property_index_label.setStyleSheet("border: 1px solid black;")
            property_name_label.setStyleSheet("border: 1px solid blue;")

            # 定义位置大小
            self.set_geo(cur_widget=property_index_label,
                         parent_widget=self.right_bottom_region,
                         x1=self.interval * 1,
                         y1=self.item_height * index,
                         width=self.label_width,
                         height=self.item_height)
            self.set_geo(cur_widget=property_name_text,
                         parent_widget=self.right_bottom_region,
                         x1=self.label_width + self.interval * 2,
                         y1=self.item_height * index,
                         width=self.short_text_width,
                         height=self.item_height)
            self.set_geo(cur_widget=property_name_label,
                         parent_widget=self.right_bottom_region,
                         x1=self.label_width + self.short_text_width + self.property_list_width + self.interval * 4,
                         y1=self.item_height * index,
                         width=self.long_label_width,
                         height=self.item_height)
            self.set_geo(cur_widget=property_value_text,
                         parent_widget=self.right_bottom_region,
                         x1=self.label_width + self.short_text_width + self.property_list_width + self.long_label_width + self.interval * 5,
                         y1=self.item_height * index,
                         width=self.label_width,
                         height=self.item_height)

            # 定义事件
            property_name_text.focus.connect(self.main_on_line_text_focus)
            property_name_text.text_change.connect(self.change_properties_list)

            property_value_text.text_change.connect(self.enable_save_button)
            property_value_text.text_change.connect(self.main_on_line_text_focus)

            self.properties_widgets_list.append(
                PropertyWidgets(property_index_label=property_index_label,
                                property_name_text=property_name_text,
                                property_name_label=property_name_label,
                                property_value_text=property_value_text)
            )

    def init_bottom_widgets(self):
        # 新增 技能文本框，按钮
        self.set_geo(cur_widget=self.new_skill_label,
                     parent_widget=self.bottom_region,
                     x1=self.interval * 0 + self.button_width * 0,
                     y1=self.button_top_margin,
                     width=self.button_width,
                     height=self.item_height
                     )
        self.new_skill_label.setText('新名称')
        self.new_skill_label.setStyleSheet(self.style_sheet)
        self.set_geo(cur_widget=self.new_skill_line_text,
                     parent_widget=self.bottom_region,
                     x1=self.interval * 1 + self.button_width * 1,
                     y1=self.button_top_margin,
                     width=self.button_width,
                     height=self.item_height
                     )
        self.set_geo(cur_widget=self.add_skill_button,
                     parent_widget=self.bottom_region,
                     x1=self.interval * 2 + self.button_width * 2,
                     y1=self.button_top_margin,
                     width=self.button_width,
                     height=self.item_height
                     )
        # 保存按钮
        self.set_geo(cur_widget=self.saveButton,
                     parent_widget=self.bottom_region,
                     x1=self.interval * 4 + self.button_width * 4,
                     y1=self.button_top_margin,
                     width=self.button_width,
                     height=self.item_height)
        self.saveButton.clicked.connect(self.save_property)
        self.add_skill_button.clicked.connect(self.add_skill_event)

    def init_property_list(self):
        self.set_geo(cur_widget=self.all_property_list_widget,
                     parent_widget=self.right_bottom_region,
                     x1=self.label_width + self.short_text_width + self.interval * 2,
                     y1=0,
                     width=self.short_text_width,
                     height=self.left_right_region_height - self.right_top_region_height)
        # 定义事件：
        self.all_property_list_widget.currentItemChanged.connect(self.all_property_list_changed)
        self.change_properties_list(index=0,text="")

    def init_skill_setting_ui(self):
        """
        # 技能设置区域
        self.setting_list=[
            # 数据库中对应的属性值，属性标签的名称，属性标签的编辑方式，可选项
            (skill.Skill.skill_name, "技能名称", "", ""),
            (skill.Skill.in_skill_store,"在商店中",EditType.combo_box,(True,False)),
            (skill.Skill.is_positive,"是否为主动技能",EditType.combo_box,(True,False)),
            (skill.Skill.effect_expression,"技能说明",EditType.text_edit,""),
        ]
        :return:
        """
        widget_index = 0
        for database_field, label_name, edit_type, choices in self.setting_list:
            col_index = widget_index % 2  # 0 or 1
            row_index = widget_index // 2  # 0,1,2,3...
            print(f'row_index {row_index},col_index:{col_index}')
            label_x1 = col_index * (self.label_width + self.short_text_width) + self.interval * col_index
            label_y1 = row_index * self.item_height

            edit_x1 = col_index * (
                    self.label_width + self.short_text_width) + self.label_width + self.interval * col_index
            edit_y1 = label_y1

            print(label_x1, label_y1, edit_y1, edit_y1)

            # label
            label = QLabel(label_name)
            self.set_geo(cur_widget=label,
                         parent_widget=self.right_top_region,
                         x1=label_x1,
                         y1=label_y1,
                         width=self.label_width,
                         height=self.item_height)

            # edit
            if edit_type == EditType.short_text:
                edit_widget = QLineEdit()
                edit_widget.setText(choices)
                self.set_geo(cur_widget=edit_widget,
                             parent_widget=self.right_top_region,
                             x1=edit_x1,
                             y1=edit_y1,
                             width=self.short_text_width,
                             height=self.item_height)
                edit_widget.textChanged.connect(self.enable_save_button)
                widget_index += 1
            elif edit_type in (EditType.long_text,):
                edit_widget = QLineEdit()
                edit_widget.setText(choices)
                self.set_geo(cur_widget=edit_widget,
                             parent_widget=self.right_top_region,
                             x1=edit_x1,
                             y1=edit_y1,
                             width=self.long_text_width,
                             height=self.item_height)
                edit_widget.textChanged.connect(self.enable_save_button)
                widget_index += 2
            elif edit_type in (EditType.combo_box,):
                edit_widget = QComboBox()
                edit_widget.addItems(choices)
                self.set_geo(cur_widget=edit_widget,
                             parent_widget=self.right_top_region,
                             x1=edit_x1,
                             y1=edit_y1,
                             width=self.short_text_width,
                             height=self.item_height)
                edit_widget.currentIndexChanged.connect(self.enable_save_button)
                widget_index += 1
            else:
                raise ValueError("暂时没有实现其他类型的edit")

            self.setting_widget_dict[database_field] = edit_widget

    def add_skill_event(self):
        new_skill_name = self.new_skill_line_text.text().strip()
        if new_skill_name == "":
            QMessageBox.information(self, '出错了！', '技能名称不可为空')
            return
        if skill.is_exists_by_name(name=new_skill_name):
            QMessageBox.information(self, '出错了！', '技能名称已经存在了')
            return
        skill.add(skill_name=new_skill_name, in_skill_store=False, is_positive=False, effect_expression='')
        self.show_all_skills()

    def main_on_line_text_focus(self, index: int, text: str):
        self.current_properties_index = index
        print(f'cur index is {self.current_properties_index}')

    def show_all_skills(self):
        # 清空之前的技能列表
        self.skillsListWidget.clear()
        skills = skill.get_all()
        for one_skill in skills:
            self.skillsListWidget.addItem(one_skill.skill_name)

    def change_properties_list(self, index: int, text: str):
        self.all_property_list_widget.clear()

        for property_name in property_cn_type_dict:
            if text not in property_name:
                continue
            self.all_property_list_widget.addItem(property_name)

    def all_property_list_changed(self, ):
        """
        用户点击了属性列表
        :return:
        """
        if not self.all_property_list_widget.currentItem():
            return
        if not self.all_property_list_widget.currentItem().text():
            return
        """
        self.property_index_label = property_index_label
        self.property_name_text = property_name_text
        self.property_name_label = property_name_label
        self.property_value_text = property_value_text"""
        property_name = self.all_property_list_widget.currentItem().text()
        self.properties_widgets_list[self.current_properties_index].property_name_text.setText(property_name)
        self.properties_widgets_list[self.current_properties_index].property_name_label.setText(property_name)

    def handle_skill_changed(self, item):
        """
        点击技能列表
        :param item:
        :return:
        """

        selected_skill_name = item.text()
        one_skill = skill.get_by_name(name=selected_skill_name)
        self.setting_widget_dict['is_positive'].setCurrentIndex(1 - sum([one_skill.is_positive]))
        self.setting_widget_dict['in_skill_store'].setCurrentIndex(1 - sum([one_skill.in_skill_store]))
        self.setting_widget_dict['effect_expression'].setText(one_skill.effect_expression)
        self.setting_widget_dict["skill_name"].setText(selected_skill_name)

        one_skill_book = skill_book.get_by_skill_id_skill_level(skill_id=one_skill.id, level=9)
        # 显示属性：
        """
        self.setting_list = [
            # 数据库中对应的属性值，属性标签的名称，属性标签的编辑方式，可选项
            ("skill_name", "技能名称", EditType.short_text, ""),
            ("level", "等级", EditType.combo_box, ("9",)),
            ("in_skill_store", "在商店中", EditType.combo_box, ("True", "False")),
            ("is_positive", "是否为主动技能", EditType.combo_box, ("True", "False")),
            ("effect_expression", "技能说明", EditType.long_text, ""),
        ]"""

        for properties_widget in self.properties_widgets_list:
            properties_widget.property_name_text.setText("")
            properties_widget.property_name_label.setText("")
            properties_widget.property_value_text.setText("")

        if one_skill_book is not None:
            skill_properties = misc_properties.get_properties_by_skill_book_id(skill_book_id=one_skill_book.id)
            for skill_property in skill_properties:
                property_name = property_type_cn_dict[skill_property.additional_property_type]
                # (property_index_label, property_name_text, property_name_label, property_value_text))
                self.properties_widgets_list[
                    skill_property.additional_source_property_index].property_name_text.setText(property_name)
                self.properties_widgets_list[
                    skill_property.additional_source_property_index].property_name_label.setText(property_name)
                self.properties_widgets_list[
                    skill_property.additional_source_property_index].property_value_text.setText(
                    str(skill_property.additional_property_value))
        # 显示保存按钮
        self.saveButton.setEnabled(False)

    def enable_save_button(self):
        self.saveButton.setEnabled(True)

    def save_property(self):
        selected_skill_name = self.skillsListWidget.currentItem().text().strip()
        new_skill_name = self.setting_widget_dict["skill_name"].text().strip()

        one_skill = skill.get_by_name(name=selected_skill_name)

        if selected_skill_name != new_skill_name:
            # 如果名字发生了修改。修改后技能的id不会发生变化
            skill.update_name_by_id(_id=one_skill.id, name=new_skill_name)
            print(f'技能名称从{selected_skill_name}->{new_skill_name}')

        skill_level = int(self.setting_widget_dict['level'].currentText())
        one_skill_book = skill_book.get_by_skill_id_skill_level(skill_id=one_skill.id, level=skill_level)

        # 如果数据库里面有对应的技能数，则进行删除，如果没有直接插入；
        if one_skill_book is not None:
            misc_properties.del_skill_book_properties(skill_book_id=one_skill_book.id)
        else:
            one_skill_book = skill_book.add(skill_id=one_skill.id, level=skill_level)

        for index, properties_widget in enumerate(self.properties_widgets_list):
            property_cn_name = properties_widget.property_name_label.text()
            property_value = properties_widget.property_value_text.text()
            if property_cn_name == "":
                continue
            if property_value == "":
                continue
            property_value = int(property_value)
            misc_properties.add_skill_book_properties(skill_book_id=one_skill_book.id,
                                                      property_index=index,
                                                      property_type=property_cn_type_dict[property_cn_name],
                                                      property_value=property_value)

            print(f"技能名称：{selected_skill_name}，第{index + 1}条属性：{property_cn_name}，属性值{property_value} 更新成功。")
        self.saveButton.setEnabled(False)  # 隐藏保存按钮
        self.show_all_skills()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
