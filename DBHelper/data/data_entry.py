import inspect
import sys
from typing import List, Dict

from sqlalchemy.orm.attributes import InstrumentedAttribute

from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QMessageBox
import sip
from sqlalchemy import Integer, String, Text, Boolean, Float

from DBHelper.db import *
from Enums import BasePropertyType, LearningApproach, SkillTarget, SkillType, SkillLevel, \
    AdditionalPropertyType, StatusType, AchievementPropertyType, AchievementType, \
    ExpBookType, DataType
from qt_utils import EditWidgetType, MyLineText, MyLabel, MyFrame, set_geo, StatuesWidgets, PropertyWidgets, MyButton, \
    TableItems, DataEdit, MyListBox, MyComboBox
from DBHelper.tables.base_table import CustomColumn as Column
from DBHelper.tables.base_table import Basic, Entity


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
        self.current_data_table_combo_box = MyComboBox()

        # 显示表中所有数据
        self.recordsListWidget = MyListBox()

        # 显示属性
        self.properties_widgets_list: List[PropertyWidgets] = []  # 包含index_label,name_text,value_text,
        self.all_property_list_widget = MyListBox()

        # 所有条目
        self.records: List[Entity] = []
        self.cur_table: Entity = None
        self.edit_items: Dict[str, DataEdit] = dict()

        # 设置区域
        self.delButton = MyButton(text='删除选中')
        self.saveButton = MyButton(text='保存')

        self.new_name_label = MyLabel()
        self.new_name_text = MyLineText()
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
        self.current_data_table_combo_box.addItem(TableItems.battle_status)
        self.current_data_table_combo_box.addItem(TableItems.base_property)
        self.current_data_table_combo_box.addItem(TableItems.achievement.name)
        self.current_data_table_combo_box.addItem(TableItems.gem)
        self.current_data_table_combo_box.setCurrentText(TableItems.achievement.name)

        self.current_data_table_combo_box.currentIndexChanged.connect(self.data_table_select_changed)

        self.data_table_select_changed(self.current_data_table_combo_box.currentIndex())

    def init_items_list(self):
        self.recordsListWidget = MyListBox()
        set_geo(cur_widget=self.recordsListWidget,
                parent_widget=self.left_region,
                x1=0,
                y1=self.item_height,
                width=self.left_region_width,
                height=self.left_right_region_height - self.item_height)

    def show_all_items(self):
        current_text = self.current_data_table_combo_box.currentText()
        table_class = TableItems.item_list.get_by_name(name=current_text).table_class

        item_names = [entity.name for entity in table_class.get_all()]

        self.records = item_names
        self.recordsListWidget.clear()
        self.recordsListWidget.addItems(item_names)

    def data_table_select_changed(self, index: int):
        print('data_table_select_changed', index)

        self.clear_temp_widgets()

        current_text = self.current_data_table_combo_box.currentText()

        table_item = TableItems.item_list.get_by_name(name=current_text)

        self.cur_table = table_item.table_class
        columns = inspect.getmembers(Achievement)

        self.edit_items.clear()

        for column in columns:
            key = column[0]
            if key == "id":
                continue
            one_column: Column = getattr(table_item.table_class, key)
            if not isinstance(one_column, InstrumentedAttribute):
                continue

            default = one_column.default
            if isinstance(one_column.type, Boolean):
                data_type = DataType.BOOL
                edit_type = EditWidgetType.bool_combo_box
            elif isinstance(one_column.type, Integer):
                data_type = DataType.INTEGER
                edit_type = EditWidgetType.short_text
            elif isinstance(one_column.type, Text):
                data_type = DataType.TEXT
                edit_type = EditWidgetType.long_text
            elif isinstance(one_column.type, String):
                data_type = DataType.STRING
                edit_type = EditWidgetType.short_text
            else:
                raise ValueError("还没有实现")
            if one_column.bind_type is not None:
                edit_type = EditWidgetType.combo_box

            new_edit_item = DataEdit(
                data_type=data_type,
                key=key,
                cn=one_column.cn,
                edit_widget_type=edit_type,
                choices=one_column.bind_type,
                editable=True,
                default=default)

            self.edit_items[key] = new_edit_item

        # if current_text == TableItems.skill:
        #     setting_list = [
        #         DataEditType(key='name', label='技能名称:', edit_widget=EditWidgetType.short_text, ),
        #         DataEditType(key='level', label='等级:', edit_widget=EditWidgetType.combo_box, choices=SkillLevel,
        #                      default=SkillLevel.NINE),
        #         DataEditType(key='learning_approach', label='学习途径:', edit_widget=EditWidgetType.combo_box,
        #                      choices=LearningApproach),
        #         DataEditType(key='skill_type', label='技能类型:', edit_widget=EditWidgetType.combo_box, choices=SkillType),
        #         DataEditType(key='target', label='作用对象:', edit_widget=EditWidgetType.combo_box, choices=SkillTarget),
        #         DataEditType(key='effect_expression', label='技能说明:', edit_widget=EditWidgetType.long_text),
        #     ]
        #     record_changed_event = self.handle_skill_changed
        #     item_add_event = self.add_skill_event
        #     item_save_event = self.save_skill_property
        #
        # elif current_text == TableItems.battle_status:  # 状态
        #     setting_list = [
        #         DataEditType(key='name', label='状态名称:', edit_widget=EditWidgetType.short_text, editable=True),
        #         DataEditType(key='status_type', label='状态类型:', edit_widget=EditWidgetType.combo_box, choices=StatusType),
        #         DataEditType(key='effect_expression', label='效果介绍:', edit_widget=EditWidgetType.long_text),
        #     ]
        #     record_changed_event = self.handle_status_changed
        #     item_add_event = self.add_status_event
        #     item_save_event = self.save_base_property
        #
        # elif current_text == TableItems.base_property:  # 状态
        #     setting_list = [
        #         DataEditType(key='name', label='基础属性', edit_widget=EditWidgetType.short_text, editable=False),
        #     ]
        #     record_changed_event = self.handle_base_property_changed
        #     item_add_event = self.add_base_property_event
        #     item_save_event = self.save_base_property
        #
        # elif current_text == TableItems.achievement:  # 成就
        #
        #
        #     setting_list = [
        #         DataEditType(key='name', label='成就名称', edit_widget=EditWidgetType.short_text),
        #         DataEditType(key='achievement_type', label='成就类型', edit_widget=EditWidgetType.combo_box,
        #                      choices=AchievementType, ),
        #
        #         DataEditType(key='condition_property_type', label='达成属性', edit_widget=EditWidgetType.combo_box,
        #                      choices=AchievementPropertyType, ),
        #         DataEditType(key='condition_property_value', label='属性值', edit_widget=EditWidgetType.short_text, ),
        #
        #         DataEditType(key='days_of_validity', label='有效期/天:', edit_widget=EditWidgetType.short_text, ),
        #         DataEditType(key='achievement_point', label='成就点数:', edit_widget=EditWidgetType.short_text, ),
        #         DataEditType(key='introduce', label='成就说明:', edit_widget=EditWidgetType.long_text, ),
        #     ]
        #     record_changed_event = self.handle_achievement_changed
        #     item_add_event = self.add_record_event
        #     item_save_event = self.save_record_record
        #
        # elif current_text == TableItems.gem:
        #     setting_list = [
        #         DataEditType(key='name', label='名称:', edit_widget=EditWidgetType.short_text, ),
        #         DataEditType(key='additional_property_type', label='属性名称:', edit_widget=EditWidgetType.combo_box,
        #                      choices=AdditionalPropertyType),
        #         DataEditType(key='increase', label='增加值:', edit_widget=EditWidgetType.short_text, ),
        #         DataEditType(key='is_bind', label='是否绑定:', edit_widget=EditWidgetType.bool_combo_box, default=False),
        #     ]
        #     record_changed_event = self.handle_gem_changed
        #     item_add_event = self.add_gem_event
        #     item_save_event = self.save_gem_event
        # elif current_text == TableItems.box:
        #     setting_list = [
        #         DataEditType(key='name', label='名称:', edit_widget=EditWidgetType.short_text, ),
        #         DataEditType(key='is_bind', label='是否绑定:', edit_widget=EditWidgetType.bool_combo_box, ),
        #         DataEditType(key='introduction', label='介绍:', edit_widget=EditWidgetType.long_text),
        #     ]
        #     record_changed_event = self.handle_box_changed
        #     item_add_event = self.add_box_event
        #     item_save_event = self.save_box_event
        # elif current_text == TableItems.exp_book:
        #     setting_list = [
        #         DataEditType(key='name', label='名称:', edit_widget=EditWidgetType.short_text, ),
        #         DataEditType(key='book_type', label='类型:', edit_widget=EditWidgetType.bool_combo_box, choices=ExpBookType),
        #         DataEditType(key='exp_value', label='经验:', edit_widget=EditWidgetType.short_text),
        #     ]
        #     record_changed_event = self.handle_exp_book_changed
        #     item_add_event = self.add_exp_book_event
        #     item_save_event = self.save_exp_book_event
        # elif current_text == TableItems.holiday:
        #     setting_list = [
        #         DataEditType(key='name', label='名称:', edit_widget=EditWidgetType.short_text),
        #         DataEditType(key='month', label='月份：', edit_widget=EditWidgetType.short_text),
        #         DataEditType(key='day', label='日期:', edit_widget=EditWidgetType.short_text),
        #     ]
        #     record_changed_event = self.handle_holiday_changed
        #     item_add_event = self.add_holiday_book
        #     item_save_event = self.save_holiday_book
        # elif current_text == TableItems.gem:
        #     ...
        # elif current_text == TableItems.identify_book:
        #     ...
        # elif current_text == TableItems.monster:
        #     ...
        # elif current_text == TableItems.monster_type_show_time:
        #     ...
        # elif current_text == TableItems.potion:
        #     ...
        # elif current_text == TableItems.raise_star_book:
        #     ...
        # elif current_text == TableItems.raise_star_prob:
        #     ...
        # elif current_text == TableItems.skill_cost_point:
        #     ...
        # elif current_text == TableItems.level_exp:
        #     ...
        # elif current_text == TableItems.player:
        #     ...
        # elif current_text == TableItems.sell_store:
        #     ...
        #
        # else:
        #     raise ValueError("还没实现其它表格的编辑")
        self.delButton.disconnect_all()
        self.delButton.clicked.connect(self.del_record)

        self.recordsListWidget.disconnect_all()
        self.recordsListWidget.currentItemChanged.connect(self.record_changed_event)

        self.show_all_items()

        self.add_entry_button.disconnect_all()
        self.add_entry_button.clicked.connect(self.add_record_event)

        self.saveButton.disconnect_all()
        self.saveButton.clicked.connect(self.save_record_record)

        self.init_item_setting_ui()
        self.update()
        self.repaint()

    def init_property_widgets(self):
        print("init_property_widgets")
        # 创建显示属性的文本框和按钮
        for index in range(self.max_property_num):
            index_label = MyLabel(f'属性：{index + 1}')
            name_text = MyLineText(index)
            # -------------------------------------
            target_label = MyLabel()
            target_combo_box = MyComboBox()
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
            target_combo_box.addItems(SkillTarget.item_list.name_index_dict.keys())
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

        horizontal_index = 0
        # 删除按钮
        set_geo(cur_widget=self.delButton,
                parent_widget=self.bottom_region,
                x1=self.interval * horizontal_index + self.button_width * horizontal_index,
                y1=self.button_top_margin,
                width=self.button_width,
                height=self.item_height)

        horizontal_index += 2
        # 新增 技能文本框，按钮
        set_geo(cur_widget=self.new_name_label,
                parent_widget=self.bottom_region,
                x1=self.interval * horizontal_index + self.button_width * horizontal_index,
                y1=self.button_top_margin,
                width=self.button_width,
                height=self.item_height
                )
        self.new_name_label.setText('新名称')

        horizontal_index += 1
        set_geo(cur_widget=self.new_name_text,
                parent_widget=self.bottom_region,
                x1=self.interval * horizontal_index + self.button_width * horizontal_index,
                y1=self.button_top_margin,
                width=self.button_width,
                height=self.item_height
                )
        horizontal_index += 1
        set_geo(cur_widget=self.add_entry_button,
                parent_widget=self.bottom_region,
                x1=self.interval * horizontal_index + self.button_width * horizontal_index,
                y1=self.button_top_margin,
                width=self.button_width,
                height=self.item_height
                )

        # 保存按钮
        horizontal_index += 1
        set_geo(cur_widget=self.saveButton,
                parent_widget=self.bottom_region,
                x1=self.interval * horizontal_index + self.button_width * horizontal_index,
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
        self.edit_items.clear()
        for item in self.right_top_region.children():
            sip.delete(item)

    def init_item_setting_ui(self):
        print("init_item_setting_ui")
        widget_index = -1
        for key in self.edit_items:
            edit_item = self.edit_items[key]
            if edit_item.edit_widget_type in {EditWidgetType.short_text, EditWidgetType.combo_box,
                                              EditWidgetType.bool_combo_box}:
                widget_index += 1
            elif edit_item.edit_widget_type in {EditWidgetType.long_text}:
                widget_index = (widget_index // 2 + 1) * 2  # 可视化的较长
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
            label = MyLabel(label_text=edit_item.cn)
            set_geo(cur_widget=label,
                    parent_widget=self.right_top_region,
                    x1=label_x1,
                    y1=label_y1,
                    width=self.label_width,
                    height=self.item_height)
            label.show()

            # edit
            if edit_item.edit_widget_type == EditWidgetType.short_text:
                edit_widget = MyLineText()
                set_geo(cur_widget=edit_widget,
                        parent_widget=self.right_top_region,
                        x1=edit_x1,
                        y1=edit_y1,
                        width=self.short_text_width,
                        height=self.item_height)
                edit_widget.set_text(text=edit_item.choices)

            elif edit_item.edit_widget_type in (EditWidgetType.long_text,):
                edit_widget = MyLineText()
                set_geo(cur_widget=edit_widget,
                        parent_widget=self.right_top_region,
                        x1=edit_x1,
                        y1=edit_y1,
                        width=self.long_text_width,
                        height=self.item_height)
                edit_widget.set_text(text=edit_item.choices)
                widget_index += 1

            elif edit_item.edit_widget_type in (EditWidgetType.combo_box,):
                edit_widget = MyComboBox()
                edit_widget.addItems(list(edit_item.choices.item_list.name_index_dict.keys()))
                edit_widget.setCurrentIndex(edit_item.choices.default.index - 1)
                set_geo(cur_widget=edit_widget,
                        parent_widget=self.right_top_region,
                        x1=edit_x1,
                        y1=edit_y1,
                        width=self.short_text_width,
                        height=self.item_height)
            elif edit_item.edit_widget_type in {EditWidgetType.bool_combo_box}:
                edit_widget = MyComboBox()
                edit_widget.addItems(["True", "False"])

                edit_widget.setEditText(str(edit_item.default))
                set_geo(cur_widget=edit_widget,
                        parent_widget=self.right_top_region,
                        x1=edit_x1,
                        y1=edit_y1,
                        width=self.short_text_width,
                        height=self.item_height)
            else:
                raise ValueError("暂时没有实现其他类型的edit")

            if edit_item.edit_widget_type in (EditWidgetType.combo_box,):
                edit_widget.currentIndexChanged.connect(self.enable_save_button)
            elif edit_item.edit_widget_type in (EditWidgetType.short_text, EditWidgetType.long_text):
                edit_widget.textChanged.connect(self.enable_save_button)

            if not edit_item.editable:
                edit_widget.setEnabled(False)
            edit_widget.show()
            self.edit_items[edit_item.key].edit_widget = edit_widget

    def add_record_event(self):
        print("add_record_event")
        new_name = self.new_name_text.text().strip()
        if new_name == "":
            QMessageBox.information(self, '出错了！', '成就不可为空')
            return
        if Achievement.is_exists_by_name(name=new_name):
            QMessageBox.information(self, '出错了！', '成就已经存在了')
            return
        self.cur_table.add_or_update_by_name(name=new_name)
        self.new_name_text.clear()
        self.show_all_items()

    def on_property_text_focus(self, index: int, text: str):
        print("on_property_text_focus")
        self.current_properties_index = index
        print(f'cur properties index is {self.current_properties_index}')

    def on_status_text_focus(self, index: int, text: str):
        print("on_status_text_focus")
        self.current_status_index = index
        print(f'cur status index is {self.current_status_index}')

    def change_properties_list(self, index: int, text: str):
        print('change_properties_list')
        self.all_property_list_widget.clear()

        for property_name in AdditionalPropertyType.item_list.name_index_dict:
            if text not in property_name:
                continue
            self.all_property_list_widget.addItem(property_name)

        # 如果属性列表的属性个数大于0并且已经加载完毕属性列表；
        if self.all_property_list_widget.count() != 0 and len(self.properties_widgets_list) > 0:
            if self.properties_widgets_list[self.current_properties_index].name_label.text() == "":
                first_item = self.all_property_list_widget.item(0)
                self.properties_widgets_list[self.current_properties_index].name_label.set_text(first_item.text())
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
        self.properties_widgets_list[self.current_properties_index].name_label.set_text(text=property_name)

    def clear_properties(self):
        for properties_widget in self.properties_widgets_list:
            properties_widget.name_text.set_text(text="")
            properties_widget.name_label.set_text(text="")
            properties_widget.value_text.set_text(text="")

    def handle_skill_changed(self, item):
        """
        点击技能列表
        """
        if item is None:
            return
        print('skill changed')
        selected_name = item.text()
        one_skill = Skill.get_by_name(name=selected_name)
        self.setting_widget_dict["name"].set_text(text=selected_name)
        self.setting_widget_dict['level'].setCurrentIndex(SkillLevel.default.index - 1)

        skill_type = one_skill.skill_type
        if not skill_type:
            skill_type = SkillType.default.index
        skill_type_cn = SkillType.item_list.index_name_dict[skill_type]
        self.setting_widget_dict['skill_type'].setCurrentText(skill_type_cn)

        learning_approach = one_skill.learning_approach
        if not one_skill.learning_approach:
            learning_approach = LearningApproach.default.index
        learning_approach_str = LearningApproach.item_list.index_name_dict[learning_approach]
        self.setting_widget_dict['learning_approach'].setCurrentText(learning_approach_str)

        effect_expression = one_skill.effect_expression
        self.setting_widget_dict['effect_expression'].set_text(text=effect_expression)

        one_skill_book = SkillBook.get_by_skill_id_skill_level(skill_id=one_skill.id, level=9)
        # 显示属性：
        self.clear_properties()

        if one_skill_book is not None:
            skill_properties = MiscProperties.get_properties_by_skill_book_id(skill_book_id=one_skill_book.id)
            for skill_property in skill_properties:
                property_name = AdditionalPropertyType.item_list.index_name_dict[
                    skill_property.additional_property_type]
                property_index = skill_property.additional_source_property_index
                self.properties_widgets_list[property_index].name_text.set_text(text=property_name)
                self.properties_widgets_list[property_index].name_label.set_text(text=property_name)
                self.properties_widgets_list[property_index].value_text.set_text(text=
                    skill_property.additional_property_value)

                property_target = skill_property.property_availability
                self.properties_widgets_list[property_index].target_combo_box.setCurrentIndex(property_target - 1)

        # 显示保存按钮
        self.saveButton.setEnabled(False)

    def handle_status_changed(self, item):
        if item is None:
            return
        print('status changed')
        selected_name = item.text()

        self.setting_widget_dict["name"].set_text(text=selected_name)
        one_status = BattleStatus.get_by_name(name=selected_name)

        self.setting_widget_dict['status_type'].setCurrentIndex(one_status.status_type - 1)
        self.setting_widget_dict['effect_expression'].set_text(text=one_status.effect_expression)

        status_properties = MiscProperties.get_properties_by_status_id(status_id=one_status.id)
        self.show_properties(properties=status_properties)

        # 显示保存按钮
        self.saveButton.setEnabled(False)

    def handle_base_property_changed(self, item):
        if item is None:  # clear的时候会触发
            return
        print('base_property changed')
        selected_name = item.text()

        self.setting_widget_dict["name"].set_text(selected_name)

        base_property_id = BasePropertyType.item_list.name_index_dict[selected_name]

        properties = MiscProperties.get_properties_by_base_property(base_property_id=base_property_id)
        self.show_properties(properties=properties)

        # 显示保存按钮
        self.saveButton.setEnabled(False)

    def record_changed_event(self, item):
        if not item:
            print("item is None")
            return

        record_name = item.text()

        record = self.cur_table.get_by_name(name=record_name)

        for key in self.edit_items:
            value = getattr(record, key)
            edit_item = self.edit_items[key]
            if edit_item.choices is not None:
                value = edit_item.choices.item_list.get_name_by_index(index=value)
            self.edit_items[key].edit_widget.set_text(text=value)

        # self.show_properties(properties=properties)
        self.saveButton.setEnabled(False)

    def handle_gem_changed(self, item):
        if not item:
            print("item is None")
            return

        print('gem changed')
        achievement_name = item.text()

        self.setting_widget_dict["name"].set_text(achievement_name)

        one_achievement = Gem.get_by_name(name=achievement_name)
        achievement_type_cn = AchievementType.item_list.index_name_dict[one_achievement.achievement_type]
        self.setting_widget_dict['achievement_type'].setCurrentText(achievement_type_cn)

        condition_property_type = one_achievement.condition_property_type
        if condition_property_type:
            condition_property_type_cn = AchievementPropertyType.item_list.index_name_dict[
                one_achievement.condition_property_type]
        else:
            condition_property_type_cn = ""
        self.setting_widget_dict['condition_property_type'].setCurrentText(condition_property_type_cn)

        condition_property_value = one_achievement.condition_property_value
        self.setting_widget_dict['condition_property_value'].set_text(text=condition_property_value)

        days_of_validity = one_achievement.days_of_validity
        self.setting_widget_dict['days_of_validity'].set_text(text=days_of_validity)

        achievement_point = one_achievement.achievement_point
        self.setting_widget_dict['achievement_point'].set_text(text=achievement_point)

        introduce = one_achievement.introduce
        self.setting_widget_dict['introduce'].set_text(text=introduce)

        properties = MiscProperties.get_properties_by_achievement_id(achievement_id=one_achievement.id)

        self.show_properties(properties=properties)
        self.saveButton.setEnabled(False)

    def handle_box_changed(self, item):
        if not item:
            print("item is None")
            return

        print('gem changed')
        achievement_name = item.text()

        self.setting_widget_dict["name"].set_text(text=achievement_name)

        one_achievement = Gem.get_by_name(name=achievement_name)
        achievement_type_cn = AchievementType.item_list.index_name_dict[one_achievement.achievement_type]
        self.setting_widget_dict['achievement_type'].setCurrentText(achievement_type_cn)

        condition_property_type = one_achievement.condition_property_type
        if condition_property_type:
            condition_property_type_cn = AchievementPropertyType.item_list.index_name_dict[
                one_achievement.condition_property_type]
        else:
            condition_property_type_cn = ""
        self.setting_widget_dict['condition_property_type'].setCurrentText(condition_property_type_cn)

        condition_property_value = one_achievement.condition_property_value
        self.setting_widget_dict['condition_property_value'].set_text(text=condition_property_value)

        days_of_validity = one_achievement.days_of_validity
        self.setting_widget_dict['days_of_validity'].set_text(text=days_of_validity)

        achievement_point = one_achievement.achievement_point
        self.setting_widget_dict['achievement_point'].set_text(text=achievement_point)

        introduce = one_achievement.introduce
        self.setting_widget_dict['introduce'].set_text(text=introduce)

        properties = MiscProperties.get_properties_by_achievement_id(achievement_id=one_achievement.id)

        self.show_properties(properties=properties)
        self.saveButton.setEnabled(False)


    def show_properties(self, *, properties: List):
        for status_property in properties:
            property_name = AdditionalPropertyType.item_list.index_name_dict[status_property.additional_property_type]
            property_index = status_property.additional_source_property_index
            self.properties_widgets_list[property_index].name_text.set_text(text=property_name)
            self.properties_widgets_list[property_index].name_label.set_text(text=property_name)
            self.properties_widgets_list[property_index].value_text.set_text(text=status_property.additional_property_value)
        # 显示保存按钮

    def enable_save_button(self):
        print("enable_save_button")
        self.saveButton.setEnabled(True)

    def save_skill_property(self):
        print("save_skill_property")
        selected_name = self.recordsListWidget.currentItem().text().strip()
        new_name = self.setting_widget_dict["name"].text().strip()
        target_name = self.setting_widget_dict["target"].currentText().strip()
        target = SkillTarget.item_list.name_index_dict[target_name]
        one_skill = Skill.get_by_name(name=selected_name)

        if selected_name != new_name:
            # 如果名字发生了修改。修改后技能的id不会发生变化
            Skill.update_name_by_id(_id=one_skill.id, new_name=new_name)
            print(f'技能名称从{selected_name}->{new_name}')

        skill_level = int(self.setting_widget_dict['level'].currentText())
        one_skill_book = SkillBook.get_by_skill_id_skill_level(skill_id=one_skill.id, level=skill_level)

        # 如果数据库里面有对应的技能书，则进行删除，如果没有直接插入；
        if one_skill_book is not None:
            MiscProperties.del_skill_book_properties(skill_book_id=one_skill_book.id)
        else:
            one_skill_book = SkillBook.add_or_update_by_id(_id=one_skill.id, level=skill_level)

        for index, properties_widget in enumerate(self.properties_widgets_list):
            property_cn_name = properties_widget.name_label.text()
            property_value = properties_widget.value_text.text()
            if property_cn_name == "":
                continue
            if property_value == "":
                continue
            property_value = int(property_value)
            MiscProperties.add_skill_book_properties(skill_book_id=one_skill_book.id,
                                                     property_index=index,
                                                     property_target=target,
                                                     property_type=AdditionalPropertyType.item_list.name_index_dict[
                                                         property_cn_name],
                                                     property_value=property_value)

            print(f"技能名称：{selected_name}，第{index + 1}条属性：{property_cn_name}，属性值{property_value} 更新成功。")
        self.saveButton.setEnabled(False)  # 隐藏保存按钮
        self.show_all_items()

    def save_status_property(self):
        print("save_status_property")

        selected_name = self.recordsListWidget.currentItem().text().strip()
        new_name = self.setting_widget_dict["name"].text().strip()
        effect_expression = self.setting_widget_dict["effect_expression"].text().strip()
        status_type = self.setting_widget_dict["status_type"].currentIndex() + 1

        one_status = BattleStatus.get_by_name(name=selected_name)

        # 如果名字发生了修改。修改后技能的id不会发生变化
        if status_type != one_status.status_type or new_name != selected_name or effect_expression != one_status.effect_expression:
            BattleStatus.add_or_update_by_id(_id=one_status.id,
                                             name=new_name,
                                             status_type=status_type,
                                             effect_expression=effect_expression)
            print(f'状态名称从{selected_name}->{new_name}')
            print(f'状态介绍从{one_status.effect_expression}->{effect_expression}')

        MiscProperties.del_status_properties(status_id=one_status.id)
        for index, properties_widget in enumerate(self.properties_widgets_list):
            property_cn_name = properties_widget.name_label.text()
            property_value = properties_widget.value_text.text()
            if property_cn_name == "":
                continue
            if property_value == "":
                continue
            property_value = int(property_value)
            MiscProperties.add_status_properties(status_id=one_status.id,
                                                 property_index=index,
                                                 property_type=AdditionalPropertyType.item_list.name_index_dict[
                                                     property_cn_name],
                                                 property_value=property_value)

            print(f"状态名称：{selected_name}，第{index + 1}条属性：{property_cn_name}，属性值{property_value} 更新成功。")
        self.saveButton.setEnabled(False)  # 隐藏保存按钮
        self.show_all_items()

    def save_base_property(self):
        print("save_base_property")

        selected_name = self.recordsListWidget.currentItem().text().strip()
        # name不会发生修改
        # 基础属性的索引
        base_property_index = BasePropertyType.item_list.name_index_dict[selected_name]

        # 删除
        MiscProperties.del_base_additional_properties(base_property_type=base_property_index)

        for index, properties_widget in enumerate(self.properties_widgets_list):
            property_cn_name = properties_widget.name_label.text()
            if property_cn_name == "":
                continue
            property_value_text = properties_widget.value_text.text()
            if property_value_text == "":
                continue
            property_num = AdditionalPropertyType.item_list.name_index_dict[property_cn_name]
            property_value = int(property_value_text)
            MiscProperties.add_base_additional_properties(
                base_property_type=base_property_index,
                additional_source_property_index=index,
                additional_property_type=property_num,
                additional_property_value=property_value,
            )
            print(f"基础属性名称：{selected_name}，第{index + 1}条属性：{property_cn_name}=属性值{property_value} 更新成功。")
        self.saveButton.setEnabled(False)  # 隐藏保存按钮
        self.show_all_items()

    def del_record(self):
        """
        删除当前选中的记录
        """
        current_name = self.recordsListWidget.currentItem().text()
        confirm = input(f"确定要删除{current_name}吗?如果确认请输出yes，输入其它内容被视为不删除。")
        if confirm == "yes":
            self.cur_table.del_by_name(name=current_name)
            print(f"删除name为 {current_name} 的记录成功！")
        self.show_all_items()

    def save_record_record(self):
        print("save_record_record")

        record: Entity = self.cur_table.get_by_name(name=self.recordsListWidget.currentItem().text())

        update_args = dict()
        for key in self.edit_items:
            data_edit = self.edit_items[key]
            value = data_edit.edit_widget.text()

            if data_edit.choices is not None:
                value = data_edit.choices.item_list.get_index_by_name(name=value)

            if data_edit.data_type == DataType.INTEGER:
                if value == "":
                    value = -1
                else:
                    value = int(value)
            elif data_edit.data_type in (DataType.STRING, DataType.TEXT):
                ...
            elif data_edit.data_type == DataType.BOOL:
                if value == "True":
                    value = True
                elif value == "False":
                    value = False
                else:
                    raise ValueError("不支持的类型")

            update_args[key] = value

        record.update_kwargs_by_id(_id=record.id, **update_args)

        # 对表格对应的属性进行操作；
        ########################################################
        # 删除对应属性
        MiscProperties.del_all_by_kwargs()
        MiscProperties.del_achievement_properties(achievement_id=cur_achievement.id)

        for index, properties_widget in enumerate(self.properties_widgets_list):
            property_cn_name = properties_widget.name_label.text()
            if property_cn_name == "":
                continue
            property_value_text = properties_widget.value_text.text()
            if property_value_text == "":
                continue
            property_num = AdditionalPropertyType.item_list.name_index_dict[property_cn_name]
            property_value = int(property_value_text)
            MiscProperties.add_achievement_properties(
                achievement_id=cur_achievement.id,
                additional_source_property_index=index,
                additional_property_type=property_num,
                additional_property_value=property_value,
            )
            print(f"成就名称名称：{selected_name}，第{index + 1}条属性：{property_cn_name}=属性值{property_value} 更新成功。")
        ########################################################

        self.saveButton.setEnabled(False)  # 隐藏保存按钮
        self.show_all_items()

    def save_gem_event(self):
        print("save_gem")

        selected_name = self.recordsListWidget.currentItem().text().strip()
        new_name = self.new_name_text.text().strip()
        # name不会发生修改
        cur_achievement = Achievement.get_by_name(name=selected_name)

        achievement_type_cn = self.setting_widget_dict['achievement_type'].currentText()
        achievement_type = AchievementType.item_list.name_index_dict[achievement_type_cn]

        condition_property_type_cn = self.setting_widget_dict['condition_property_type'].currentText()
        condition_property_type = AchievementPropertyType.item_list.name_index_dict[condition_property_type_cn]

        condition_property_value = self.setting_widget_dict['condition_property_value'].text()

        days_of_validity = int(self.setting_widget_dict['days_of_validity'].text())
        achievement_point = int(self.setting_widget_dict['achievement_point'].text())

        introduce = self.setting_widget_dict['introduce'].text()

        Achievement.add_or_update_by_id(_id=cur_achievement.id,
                                        achievement_type=achievement_type,
                                        name=new_name,

                                        condition_type=condition_property_type,
                                        condition_value=condition_property_value,

                                        days_of_validity=days_of_validity,
                                        achievement_point=achievement_point,

                                        introduce=introduce
                                        )



    def save_box_event(self):
        print("save_box")

        selected_name = self.recordsListWidget.currentItem().text().strip()
        new_name = self.new_name_text.text().strip()
        # name不会发生修改
        cur_achievement = Achievement.get_by_name(name=selected_name)

        achievement_type_cn = self.setting_widget_dict['achievement_type'].currentText()
        achievement_type = AchievementType.item_list.name_index_dict[achievement_type_cn]

        condition_property_type_cn = self.setting_widget_dict['condition_property_type'].currentText()
        condition_property_type = AchievementPropertyType.item_list.name_index_dict[condition_property_type_cn]

        condition_property_value = self.setting_widget_dict['condition_property_value'].text()

        days_of_validity = int(self.setting_widget_dict['days_of_validity'].text())
        achievement_point = int(self.setting_widget_dict['achievement_point'].text())

        introduce = self.setting_widget_dict['introduce'].text()

        Achievement.update(achievement_id=cur_achievement.id,
                           new_achievement_type=achievement_type,
                           new_name=new_name,

                           new_condition_type=condition_property_type,
                           new_condition_value=condition_property_value,

                           new_days_of_validity=days_of_validity,
                           new_achievement_point=achievement_point,

                           new_introduce=introduce
                           )

        # 删除
        MiscProperties.del_achievement_properties(achievement_id=cur_achievement.id)

        for index, properties_widget in enumerate(self.properties_widgets_list):
            property_cn_name = properties_widget.name_label.text()
            if property_cn_name == "":
                continue
            property_value_text = properties_widget.value_text.text()
            if property_value_text == "":
                continue
            property_num = AdditionalPropertyType.item_list.name_index_dict[property_cn_name]
            property_value = int(property_value_text)
            MiscProperties.add_achievement_properties(
                achievement_id=cur_achievement.id,
                additional_source_property_index=index,
                additional_property_type=property_num,
                additional_property_value=property_value,
            )
            print(f"成就名称名称：{selected_name}，第{index + 1}条属性：{property_cn_name}=属性值{property_value} 更新成功。")
        self.saveButton.setEnabled(False)  # 隐藏保存按钮
        self.show_all_items()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
