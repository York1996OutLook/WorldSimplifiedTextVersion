import sys
from collections import defaultdict

import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QListWidget, QMessageBox, QComboBox
from PyQt5.QtCore import pyqtSignal, pyqtBoundSignal
import PyQt5.QtGui as QtGui
import sip

from DBHelper.db import *
from Enums import BasePropertyType, LearningApproach, SkillTarget, SkillType, SkillLevel, AdditionSourceType, \
    AdditionalPropertyType, \
    StatusType
from qt_utils import EditType, MyLineText, MyLabel, MyFrame, set_geo, StatuesWidgets, PropertyWidgets, MyButton, \
    TableItems


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        print('__init__')
        self.left_region_width = 160
        self.bottom_region_height = 60
        self.item_height = 35

        self.label_width = 60  # 属性1，属性2，
        self.long_label_width = 100  # 具体属性名字展示

        self.short_text_width = 100  # 具体属性名字输入
        self.long_text_width = 300  # 具体属性名字输入

        self.right_top_region_height = 200
        self.right_middle_region_height = 210
        self.right_bottom_region_height = 200

        self.left_right_region_height = self.right_top_region_height + self.right_middle_region_height + self.right_bottom_region_height

        self.button_width = 100
        self.button_top_margin = 10

        self.property_list_width = 120
        self.statues_list_width = 150
        self.interval = 6

        self.max_property_num = 6
        # 区域划分
        self.left_region = MyFrame()
        self.right_region = MyFrame()

        self.right_top_region = MyFrame()
        self.right_middle_region = MyFrame()
        self.right_bottom_region = MyFrame()

        self.bottom_region = MyFrame()

        # 选择修改哪个表格
        self.current_data_table_label = MyLabel()
        self.current_data_table_combo_box = QComboBox()

        # 显示表中所有数据
        self.itemsListWidget = QListWidget()

        # 显示属性
        self.properties_widgets_list = []  # 包含index_label,name_text,value_text,
        self.all_property_list_widget = QListWidget()

        # 设置区域
        self.setting_list = []

        self.setting_widget_dict = dict()

        self.saveButton = MyButton(text='保存')

        self.new_name_label = MyLabel()
        self.new_name_text = QLineEdit()
        self.add_entry_button = MyButton(text="新增")

        self.current_properties_index = 0
        self.current_status_index = 0

        self.initUI()

    def initUI(self):
        print('init UI')
        right_region_width = 600

        left_right_region_width = self.left_region_width + right_region_width

        self.setWindowTitle('属性表:')
        self.setGeometry(0,
                         0,
                         left_right_region_width,
                         self.left_right_region_height + self.bottom_region_height)

        # 左
        set_geo(cur_widget=self.left_region,
                parent_widget=self,
                x1=0,
                y1=0,
                width=self.left_region_width,
                height=self.left_right_region_height)
        # 右边
        set_geo(cur_widget=self.right_region,
                parent_widget=self,
                x1=self.left_region_width,
                y1=0,
                width=right_region_width, height=self.left_right_region_height)

        # 右上
        set_geo(cur_widget=self.right_top_region,
                parent_widget=self.right_region,
                x1=0,
                y1=0,
                width=right_region_width, height=self.right_top_region_height)
        # 右中
        set_geo(cur_widget=self.right_middle_region,
                parent_widget=self.right_region,
                x1=0,
                y1=self.right_top_region_height,
                width=right_region_width, height=self.right_middle_region_height)
        # 右下
        set_geo(cur_widget=self.right_bottom_region,
                parent_widget=self.right_region,
                x1=0,
                y1=self.right_top_region_height + self.right_middle_region_height,
                width=right_region_width, height=self.right_top_region_height)
        # 下方
        set_geo(cur_widget=self.bottom_region,
                parent_widget=self,
                x1=0,
                y1=self.left_right_region_height,
                width=left_right_region_width,
                height=self.bottom_region_height,
                )
        # 所有项目都会加载的列表框
        self.init_items_list()

        self.init_select_current_table()
        self.init_property_list()
        self.init_property_widgets()
        self.init_bottom_widgets()

    def init_select_current_table(self):
        print('init init_select_current_table')
        set_geo(cur_widget=self.current_data_table_label,
                parent_widget=self.left_region,
                x1=0,
                y1=0,
                width=self.label_width,
                height=self.item_height)
        self.current_data_table_label.setText('当前表：')

        set_geo(cur_widget=self.current_data_table_combo_box,
                parent_widget=self.left_region,
                x1=self.label_width,
                y1=0,
                width=self.button_width,
                height=self.item_height)
        self.current_data_table_combo_box.addItem(TableItems.skill)
        self.current_data_table_combo_box.addItem(TableItems.status)
        self.current_data_table_combo_box.addItem(TableItems.base_property)
        self.current_data_table_combo_box.setCurrentText(TableItems.base_property)

        self.current_data_table_combo_box.currentIndexChanged.connect(self.data_table_select_changed)
        
        self.data_table_select_changed(self.current_data_table_combo_box.currentIndex())

    def init_items_list(self):
        self.itemsListWidget = QListWidget()
        set_geo(cur_widget=self.itemsListWidget,
                parent_widget=self.left_region,
                x1=0,
                y1=self.item_height,
                width=self.left_region_width,
                height=self.left_right_region_height - self.item_height)

    def load_skill_UI(self):
        print('load_skill_UI')
        self.clear_temp_widgets()
        self.setting_list = [
            # 数据库中对应的属性值，属性标签的名称，属性标签的编辑方式，可选项,是否可以编辑
            ("skill_name", "技能名称:", EditType.short_text, "", True),
            ("level", "等级:", EditType.combo_box, SkillLevel, False),
            ("learning_approach", "学习途径:", EditType.combo_box, LearningApproach(), True),
            ("skill_type", "技能类型:", EditType.combo_box, SkillType, True),
            ("target", "作用对象", EditType.combo_box, SkillTarget, True),
            ("effect_expression", "技能说明:", EditType.long_text, "", True),
        ]
        self.init_skill_list_widget()

        self.add_entry_button.disconnect_all()
        self.add_entry_button.clicked.connect(self.add_skill_event)

        self.saveButton.disconnect_all()
        self.saveButton.clicked.connect(self.save_skill_property)

    def load_status_UI(self):
        print('load_status_UI')
        self.clear_temp_widgets()
        self.setting_list = [
            # 数据库中对应的属性值，属性标签的名称，属性标签的编辑方式，可选项,是否可以编辑
            ("name", "状态名称:", EditType.short_text, "", True),
            ("status_type", "状态类型:", EditType.combo_box, StatusType, True),
            ("effect_expression", "效果介绍:", EditType.long_text, "", True),
        ]
        self.init_status_list_widget()

        self.add_entry_button.disconnect_all()
        self.add_entry_button.clicked.connect(self.add_status_event)

        self.saveButton.disconnect_all()
        self.saveButton.clicked.connect(self.save_status_property)

    def load_base_property_UI(self):
        print('load_status_UI')
        self.clear_temp_widgets()
        self.setting_list = [
            ("name", "基础属性:", EditType.short_text, "", False),
        ]
        self.init_base_property_list_widget()

        self.add_entry_button.disconnect_all()
        self.add_entry_button.clicked.connect(self.add_base_property_event)

        self.saveButton.disconnect_all()
        self.saveButton.clicked.connect(self.save_base_property)

    def load_achievement_UI(self):
        print('load_achievement_UI')
        self.clear_temp_widgets()
        self.setting_list = [
            # 数据库中对应的属性值，属性标签的名称，属性标签的编辑方式，可选项,是否可以编辑
            ("name", "成就名称:", EditType.short_text, "", True),
            ("achievement_type", "成就类型:", EditType.combo_box, SkillLevel, True),

            ("condition_property_type", "达成属性:", EditType.combo_box, LearningApproach, True),
            ("condition_property_value", "属性值:", EditType.short_text, SkillType, True),

            ("days_of_validity", "有效期/天:", EditType.short_text, SkillTarget, True),
            ("introduce", "成就说明:", EditType.long_text, "", True),
        ]
        self.init_achievement_list_widget()

        self.add_entry_button.disconnect_all()
        self.add_entry_button.clicked.connect(self.add_skill_event)

        self.saveButton.disconnect_all()
        self.saveButton.clicked.connect(self.save_skill_property)

    def data_table_select_changed(self, index: int):
        print('data_table_select_changed', index)
        current_text = self.current_data_table_combo_box.currentText()
        
        if current_text == TableItems.skill:  # 技能
            self.load_skill_UI()
        elif current_text == TableItems.status:  # 状态
            self.load_status_UI()
        elif current_text == TableItems.base_property:  # 状态
            self.load_base_property_UI()
        elif current_text == TableItems.achievement:  # 成就
            ...
        self.init_item_setting_ui()
        self.update()
        self.repaint()

    def init_skill_list_widget(self):
        print('init_skill_list_widget')
        # 创建显示技能的列表

        self.itemsListWidget.itemClicked.connect(self.handle_skill_changed)
        self.itemsListWidget.setFixedWidth(self.left_region_width)
        self.show_all_skills()
        self.itemsListWidget.show()

    def init_status_list_widget(self):
        print('init_status_list_widget')
        self.itemsListWidget.itemClicked.connect(self.handle_status_changed)
        self.itemsListWidget.setFixedWidth(self.left_region_width)
        self.show_all_status()
        self.itemsListWidget.show()

    def init_base_property_list_widget(self):
        print('init_base_property_list_widget')
        self.itemsListWidget.itemClicked.connect(self.handle_base_property_changed)
        
        self.itemsListWidget.setFixedWidth(self.left_region_width)
        self.show_all_base_properties()
        self.itemsListWidget.show()

    def init_achievement_list_widget(self):
        print('init_achievement_list_widget')

        self.itemsListWidget.itemClicked.connect(self.handle_base_property_changed)
        self.itemsListWidget.setFixedWidth(self.left_region_width)
        self.show_all_base_properties()
        self.itemsListWidget.show()

    def init_property_widgets(self):
        print("init_property_widgets")
        # 创建显示属性的文本框和按钮
        for index in range(self.max_property_num):
            index_label = MyLabel(f'属性：{index + 1}')
            name_text = MyLineText(index)
            # -------------------------------------
            target_label = MyLabel()
            target_combo_box = QComboBox()
            # -------------------------------------
            name_label = MyLabel()
            value_text = MyLineText(index)

            # 定义位置大小
            set_geo(cur_widget=index_label,
                    parent_widget=self.right_middle_region,
                    x1=self.interval * 1,
                    y1=self.item_height * index,
                    width=self.label_width,
                    height=self.item_height)
            set_geo(cur_widget=name_text,
                    parent_widget=self.right_middle_region,
                    x1=index_label.x() + index_label.width() + self.interval,
                    y1=self.item_height * index,
                    width=self.short_text_width,
                    height=self.item_height)

            set_geo(cur_widget=target_label,
                    parent_widget=self.right_middle_region,
                    x1=self.all_property_list_widget.x() + self.all_property_list_widget.width() + self.interval,
                    y1=self.item_height * index,
                    width=self.label_width,
                    height=self.item_height)
            set_geo(cur_widget=target_combo_box,
                    parent_widget=self.right_middle_region,
                    x1=target_label.x() + target_label.width() + self.interval,
                    y1=self.item_height * index,
                    width=self.label_width,
                    height=self.item_height)

            set_geo(cur_widget=name_label,
                    parent_widget=self.right_middle_region,
                    x1=target_combo_box.x() + target_combo_box.width() + self.interval,
                    y1=self.item_height * index,
                    width=self.long_label_width,
                    height=self.item_height)

            set_geo(cur_widget=value_text,
                    parent_widget=self.right_middle_region,
                    x1=name_label.x() + name_label.width() + self.interval,
                    y1=self.item_height * index,
                    width=self.label_width,
                    height=self.item_height)
            # 设置内容
            target_label.setText("作用对象：")
            target_combo_box.addItems(SkillTarget.name_index_dict.keys())
            target_combo_box.setCurrentIndex(SkillTarget.default.index)

            # 定义事件
            name_text.focus.connect(self.on_property_text_focus)
            name_text.focus.connect(self.change_properties_list)
            name_text.text_change.connect(self.change_properties_list)

            value_text.text_change.connect(self.enable_save_button)
            value_text.text_change.connect(self.on_property_text_focus)

            self.properties_widgets_list.append(
                PropertyWidgets(index_label=index_label,
                                name_text=name_text,
                                target_label=target_label,
                                target_combo_box=target_combo_box,
                                name_label=name_label,
                                value_text=value_text)
            )

    def init_bottom_widgets(self):
        print("init_bottom_widgets")
        # 新增 技能文本框，按钮
        set_geo(cur_widget=self.new_name_label,
                parent_widget=self.bottom_region,
                x1=self.interval * 0 + self.button_width * 0,
                y1=self.button_top_margin,
                width=self.button_width,
                height=self.item_height
                )
        self.new_name_label.setText('新名称')

        set_geo(cur_widget=self.new_name_text,
                parent_widget=self.bottom_region,
                x1=self.interval * 1 + self.button_width * 1,
                y1=self.button_top_margin,
                width=self.button_width,
                height=self.item_height
                )

        set_geo(cur_widget=self.add_entry_button,
                parent_widget=self.bottom_region,
                x1=self.interval * 2 + self.button_width * 2,
                y1=self.button_top_margin,
                width=self.button_width,
                height=self.item_height
                )
        # 保存按钮
        set_geo(cur_widget=self.saveButton,
                parent_widget=self.bottom_region,
                x1=self.interval * 4 + self.button_width * 4,
                y1=self.button_top_margin,
                width=self.button_width,
                height=self.item_height)

    def init_status_list(self):
        print("init_status_list")
        # 创建显示附加属性的显示列表
        for index in range(4):
            statues_index_label = MyLabel(f'状态：{index + 1}')
            statues_name_text = MyLineText(index)
            # -------------------------------------
            statues_name_label = MyLabel()

            # 定义位置大小
            set_geo(cur_widget=statues_index_label,
                    parent_widget=self.right_bottom_region,
                    x1=self.interval * 1,
                    y1=self.item_height * index,
                    width=self.label_width,
                    height=self.item_height)
            set_geo(cur_widget=statues_name_text,
                    parent_widget=self.right_bottom_region,
                    x1=self.label_width + self.interval * 2,
                    y1=self.item_height * index,
                    width=self.short_text_width,
                    height=self.item_height)
            set_geo(cur_widget=statues_name_label,
                    parent_widget=self.right_bottom_region,
                    x1=self.label_width + self.short_text_width + self.statues_list_width + self.interval * 4,
                    y1=self.item_height * index,
                    width=self.long_label_width,
                    height=self.item_height)

            # 定义事件
            statues_name_text.focus.connect(self.on_property_text_focus)
            statues_name_text.text_change.connect(self.change_properties_list)

            self.properties_widgets_list.append(
                StatuesWidgets(statues_index_label=statues_index_label,
                               statues_name_text=statues_name_text,
                               statues_name_label=statues_name_label,
                               )
            )

    def init_property_list(self):
        print("init_property_list")
        set_geo(cur_widget=self.all_property_list_widget,
                parent_widget=self.right_middle_region,
                x1=self.label_width + self.short_text_width + self.interval * 2,
                y1=0,
                width=self.property_list_width,
                height=self.right_middle_region_height)
        # 定义事件：
        self.all_property_list_widget.currentItemChanged.connect(self.all_property_list_changed)
        self.all_property_list_widget.currentItemChanged.connect(self.enable_save_button)
        self.change_properties_list(index=0, text="")

    def clear_temp_widgets(self):
        print("clear_temp_widgets")
        self.setting_widget_dict.clear()
        sip.delete(self.itemsListWidget)
        for item in self.right_top_region.children():
            sip.delete(item)

    def init_item_setting_ui(self):
        print("init_item_setting_ui")
        widget_index = -1
        for database_field, label_name, edit_type, choices, changeable in self.setting_list:
            if edit_type in {EditType.short_text, EditType.combo_box}:
                widget_index += 1
            elif edit_type in {EditType.long_text}:
                widget_index = (widget_index // 2 + 1) * 2
            else:
                raise ValueError()

            # 在数据库中的字段，标签的名字，编辑类型（文本框还是组合框）,可选项，是否可以编辑
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
            label = MyLabel(label_text=label_name)
            set_geo(cur_widget=label,
                    parent_widget=self.right_top_region,
                    x1=label_x1,
                    y1=label_y1,
                    width=self.label_width,
                    height=self.item_height)
            label.show()

            # edit
            if edit_type == EditType.short_text:
                edit_widget = QLineEdit()
                edit_widget.setText(choices)
                set_geo(cur_widget=edit_widget,
                        parent_widget=self.right_top_region,
                        x1=edit_x1,
                        y1=edit_y1,
                        width=self.short_text_width,
                        height=self.item_height)

            elif edit_type in (EditType.long_text,):
                edit_widget = QLineEdit()
                edit_widget.setText(choices)
                set_geo(cur_widget=edit_widget,
                        parent_widget=self.right_top_region,
                        x1=edit_x1,
                        y1=edit_y1,
                        width=self.long_text_width,
                        height=self.item_height)

            elif edit_type in (EditType.combo_box,):
                edit_widget = QComboBox()
                edit_widget.addItems(list(choices.name_index_dict.keys()))
                edit_widget.setCurrentIndex(choices.default.index - 1)
                set_geo(cur_widget=edit_widget,
                        parent_widget=self.right_top_region,
                        x1=edit_x1,
                        y1=edit_y1,
                        width=self.short_text_width,
                        height=self.item_height)
            else:
                raise ValueError("暂时没有实现其他类型的edit")

            if edit_type in (EditType.combo_box,):
                edit_widget.currentIndexChanged.connect(self.enable_save_button)
            elif edit_type in (EditType.short_text, EditType.long_text):
                edit_widget.textChanged.connect(self.enable_save_button)

            if not changeable:
                edit_widget.setEnabled(False)
            edit_widget.show()
            self.setting_widget_dict[database_field] = edit_widget
            self.setting_widget_dict[f'{database_field}_choices'] = choices

    def add_skill_event(self):
        print("add_skill_event")
        new_name = self.new_name_text.text().strip()
        if new_name == "":
            QMessageBox.information(self, '出错了！', '技能名称不可为空')
            return
        if skill.is_exists_by_name(name=new_name):
            QMessageBox.information(self, '出错了！', '技能名称已经存在了')
            return
        skill.add(skill_name=new_name)
        self.show_all_skills()

    def add_status_event(self):
        print("add_status_event")
        new_name = self.new_name_text.text().strip()
        if new_name == "":
            QMessageBox.information(self, '出错了！', '技能名称不可为空')
            return
        if battle_status.is_exists_by_name(name=new_name):
            QMessageBox.information(self, '出错了！', '技能名称已经存在了')
            return
        battle_status.add(name=new_name)
        self.new_name_text.clear()
        self.show_all_status()

    def add_base_property_event(self):
        print("add_status_event")
        QMessageBox.information(self, '出错了！', '基础属性对应其他属性加成不可以修改！')

    def on_property_text_focus(self, index: int, text: str):
        print("on_property_text_focus")
        self.current_properties_index = index
        print(f'cur properties index is {self.current_properties_index}')

    def on_status_text_focus(self, index: int, text: str):
        print("on_status_text_focus")
        self.current_status_index = index
        print(f'cur status index is {self.current_status_index}')

    def show_all_skills(self):
        print("show_all_skills")
        # 清空之前的技能列表
        self.itemsListWidget.clear()
        skills = skill.get_all()
        for one_skill in skills:
            self.itemsListWidget.addItem(one_skill.skill_name)

    def show_all_status(self):
        print("show_all_status")
        # 清空之前的技能列表
        self.itemsListWidget.clear()
        status = battle_status.get_all()
        for one_status in status:
            self.itemsListWidget.addItem(one_status.name)

    def show_all_base_properties(self):
        print("show_all_base_properties")
        # 清空之前的技能列表
        self.itemsListWidget.clear()
        base_properties = BasePropertyType.name_index_dict.keys()
        self.itemsListWidget.addItems(base_properties)

    def change_properties_list(self, index: int, text: str):
        print('change_properties_list')
        self.all_property_list_widget.clear()

        for property_name in AdditionalPropertyType.name_index_dict:
            if text not in property_name:
                continue
            self.all_property_list_widget.addItem(property_name)

        # 如果属性列表的属性个数大于0并且已经加载完毕属性列表；
        if self.all_property_list_widget.count() != 0 and len(self.properties_widgets_list) > 0:
            if self.properties_widgets_list[self.current_properties_index].name_label.text() == "":
                first_item = self.all_property_list_widget.item(0)
                self.properties_widgets_list[self.current_properties_index].name_label.setText(first_item.text())
        self.enable_save_button()

    def all_property_list_changed(self, ):
        """
        用户点击了属性列表
        :return:
        """
        print("all_property_list_changed")
        if not self.all_property_list_widget.currentItem():
            return
        if not self.all_property_list_widget.currentItem().text():
            return
        """
        self.index_label = index_label
        self.name_text = name_text
        self.name_label = name_label
        self.value_text = value_text"""
        property_name = self.all_property_list_widget.currentItem().text()
        self.properties_widgets_list[self.current_properties_index].name_label.setText(property_name)

    def handle_skill_changed(self, item):
        """
        点击技能列表
        :param item:
        :return:
        """
        print('skill changed')
        selected_name = item.text()
        one_skill = skill.get_by_name(name=selected_name)
        self.setting_widget_dict["skill_name"].setText(selected_name)
        self.setting_widget_dict['level'].setCurrentIndex(SkillLevel.default.index - 1)
        if one_skill.skill_type is not None:
            index = one_skill.skill_type - 1
        else:
            index = SkillType.default.index - 1
        self.setting_widget_dict['skill_type'].setCurrentIndex(index)

        if one_skill.learning_approach is not None:
            index = one_skill.learning_approach - 1
        else:
            index = LearningApproach.default.index - 1
        self.setting_widget_dict['learning_approach'].setCurrentIndex(index)
        self.setting_widget_dict['effect_expression'].setText(one_skill.effect_expression)

        one_skill_book = skill_book.get_by_skill_id_skill_level(skill_id=one_skill.id, level=9)
        # 显示属性：
        """
        self.setting_list = [
            # 数据库中对应的属性值，属性标签的名称，属性标签的编辑方式，可选项
            ("skill_name", "技能名称", EditType.short_text, ""),
            ("level", "等级", EditType.combo_box, ("9",)),
            ("learning_approach", "学习途径", EditType.combo_box, SkillLearnable),
            ("skill_type", "技能类型", EditType.combo_box, SkillType),
            ("target", "作用对象", EditType.combo_box, SkillTarget),
            ("effect_expression", "技能说明", EditType.long_text, ""),
        ]"""

        for properties_widget in self.properties_widgets_list:
            properties_widget.name_text.setText("")
            properties_widget.name_label.setText("")
            properties_widget.value_text.setText("")

        if one_skill_book is not None:
            skill_properties = misc_properties.get_properties_by_skill_book_id(skill_book_id=one_skill_book.id)
            for skill_property in skill_properties:
                property_name = AdditionalPropertyType.index_name_dict[skill_property.additional_property_type]
                # (index_label, name_text, name_label, value_text))
                property_index = skill_property.additional_source_property_index
                self.properties_widgets_list[property_index].name_text.setText(property_name)
                self.properties_widgets_list[property_index].name_label.setText(property_name)

                property_target = skill_property.property_availability
                self.properties_widgets_list[property_index].target_combo_box.setCurrentIndex(property_target - 1)

                self.properties_widgets_list[property_index].value_text.setText(
                    str(skill_property.additional_property_value))
        # 显示保存按钮
        self.saveButton.setEnabled(False)

    def handle_status_changed(self, item):
        """
        self.setting_list = [
            # 数据库中对应的属性值，属性标签的名称，属性标签的编辑方式，可选项
            ("name", "状态名称", EditType.short_text, ""),
            ("effect", "效果介绍", EditType.long_text, ""),
        ]
        :param item:
        :return:
        """
        print('status changed')
        selected_status_name = item.text()

        self.setting_widget_dict["name"].setText(selected_status_name)
        one_status = battle_status.get_by_name(name=selected_status_name)

        self.setting_widget_dict['status_type'].setCurrentIndex(one_status.status_type - 1)
        self.setting_widget_dict['effect_expression'].setText(one_status.effect_expression)

        for properties_widget in self.properties_widgets_list:
            properties_widget.name_text.setText("")
            properties_widget.name_label.setText("")
            properties_widget.value_text.setText("")

        if one_status is not None:
            status_properties = misc_properties.get_properties_by_status_id(status_id=one_status.id)
            for status_property in status_properties:
                property_name = AdditionalPropertyType.index_name_dict[status_property.additional_property_type]
                # (index_label, name_text, name_label, value_text))
                property_index = status_property.additional_source_property_index
                self.properties_widgets_list[property_index].name_text.setText(property_name)
                self.properties_widgets_list[property_index].name_label.setText(property_name)
                self.properties_widgets_list[property_index].value_text.setText(
                    str(status_property.additional_property_value))
        # 显示保存按钮
        self.saveButton.setEnabled(False)

    def handle_base_property_changed(self, item):
        """
        self.setting_list = [
            # 数据库中对应的属性值，属性标签的名称，属性标签的编辑方式，可选项
            ("name", "状态名称", EditType.short_text, ""),
            ("effect", "效果介绍", EditType.long_text, ""),
        ]
        :param item:
        :return:
        """
        print('base_property changed')
        selected_status_name = item.text()

        self.setting_widget_dict["name"].setText(selected_status_name)

        for properties_widget in self.properties_widgets_list:
            properties_widget.name_text.setText("")
            properties_widget.name_label.setText("")
            properties_widget.value_text.setText("")

        base_property_id = BasePropertyType.name_index_dict[selected_status_name]

        status_properties = misc_properties.get_properties_by_base_property(base_property_id=base_property_id)
        for status_property in status_properties:
            property_name = AdditionalPropertyType.index_name_dict[status_property.additional_property_type]
            property_index = status_property.additional_source_property_index
            self.properties_widgets_list[property_index].name_text.setText(property_name)
            self.properties_widgets_list[property_index].name_label.setText(property_name)
            self.properties_widgets_list[property_index].value_text.setText(
                str(status_property.additional_property_value))
        # 显示保存按钮
        self.saveButton.setEnabled(False)

    def enable_save_button(self):
        print("enable_save_button")
        self.saveButton.setEnabled(True)

    def save_skill_property(self):
        print("save_skill_property")
        selected_name = self.itemsListWidget.currentItem().text().strip()
        new_name = self.setting_widget_dict["skill_name"].text().strip()
        target_name = self.setting_widget_dict["target"].currentText().strip()
        target = SkillTarget.name_index_dict[target_name]
        """
            # 数据库中对应的属性值，属性标签的名称，属性标签的编辑方式，可选项
            ("skill_name", "技能名称", EditType.short_text, ""),
            ("level", "等级", EditType.combo_box, ("9",)),
            ("learning_approach", "学习途径", EditType.combo_box, SkillLearnable),
            ("skill_type", "技能类型", EditType.combo_box, SkillType),
            ("target", "作用对象", EditType.combo_box, SkillTarget),
            ("effect_expression", "技能说明", EditType.long_text, ""),"""
        one_skill = skill.get_by_name(name=selected_name)

        if selected_name != new_name:
            # 如果名字发生了修改。修改后技能的id不会发生变化
            skill.update_name_by_id(_id=one_skill.id, name=new_name)
            print(f'技能名称从{selected_name}->{new_name}')

        skill_level = int(self.setting_widget_dict['level'].currentText())
        one_skill_book = skill_book.get_by_skill_id_skill_level(skill_id=one_skill.id, level=skill_level)

        # 如果数据库里面有对应的技能数，则进行删除，如果没有直接插入；
        if one_skill_book is not None:
            misc_properties.del_skill_book_properties(skill_book_id=one_skill_book.id)
        else:
            one_skill_book = skill_book.add(skill_id=one_skill.id, level=skill_level)

        for index, properties_widget in enumerate(self.properties_widgets_list):
            property_cn_name = properties_widget.name_label.text()
            property_value = properties_widget.value_text.text()
            if property_cn_name == "":
                continue
            if property_value == "":
                continue
            property_value = int(property_value)
            misc_properties.add_skill_book_properties(skill_book_id=one_skill_book.id,
                                                      property_index=index,
                                                      property_target=target,
                                                      property_type=AdditionalPropertyType.name_index_dict[
                                                          property_cn_name],
                                                      property_value=property_value)

            print(f"技能名称：{selected_name}，第{index + 1}条属性：{property_cn_name}，属性值{property_value} 更新成功。")
        self.saveButton.setEnabled(False)  # 隐藏保存按钮
        self.show_all_skills()

    def save_status_property(self):
        print("save_status_property")

        selected_name = self.itemsListWidget.currentItem().text().strip()
        new_name = self.setting_widget_dict["name"].text().strip()
        effect_expression = self.setting_widget_dict["effect_expression"].text().strip()
        status_type = self.setting_widget_dict["status_type"].currentIndex() + 1

        one_status = battle_status.get_by_name(name=selected_name)

        # 如果名字发生了修改。修改后技能的id不会发生变化
        if status_type != one_status.status_type or new_name != selected_name or effect_expression != one_status.effect_expression:
            battle_status.update_by_id(battle_status_id=one_status.id,
                                       name=new_name,
                                       status_type=status_type,
                                       effect_expression=effect_expression)
            print(f'状态名称从{selected_name}->{new_name}')
            print(f'状态介绍从{one_status.effect_expression}->{effect_expression}')

        misc_properties.del_status_properties(status_id=one_status.id)
        for index, properties_widget in enumerate(self.properties_widgets_list):
            property_cn_name = properties_widget.name_label.text()
            property_value = properties_widget.value_text.text()
            if property_cn_name == "":
                continue
            if property_value == "":
                continue
            property_value = int(property_value)
            misc_properties.add_status_properties(status_id=one_status.id,
                                                  property_index=index,
                                                  property_type=AdditionalPropertyType.name_index_dict[
                                                      property_cn_name],
                                                  property_value=property_value)

            print(f"状态名称：{selected_name}，第{index + 1}条属性：{property_cn_name}，属性值{property_value} 更新成功。")
        self.saveButton.setEnabled(False)  # 隐藏保存按钮
        self.show_all_status()

    def save_base_property(self):
        print("save_base_property")

        selected_name = self.itemsListWidget.currentItem().text().strip()
        # name不会发生修改
        # 基础属性的索引
        base_property_index = BasePropertyType.name_index_dict[selected_name]

        # 删除
        misc_properties.del_base_additional_properties(base_property_type=base_property_index)

        for index, properties_widget in enumerate(self.properties_widgets_list):
            property_cn_name = properties_widget.name_label.text()
            if property_cn_name == "":
                continue
            property_value_text = properties_widget.value_text.text()
            if property_value_text == "":
                continue
            property_num = AdditionalPropertyType.name_index_dict[property_cn_name]
            property_value = int(property_value_text)
            misc_properties.add_base_additional_properties(
                base_property_type=base_property_index,
                property_index=index,
                additional_property_type=property_num,
                additional_property_value=property_value,
            )
            print(f"基础属性名称：{selected_name}，第{index + 1}条属性：{property_cn_name}=属性值{property_value} 更新成功。")
        self.saveButton.setEnabled(False)  # 隐藏保存按钮
        self.show_all_base_properties()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
