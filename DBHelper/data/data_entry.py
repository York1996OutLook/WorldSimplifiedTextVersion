import inspect
import sys
from typing import List, Dict

from sqlalchemy.orm.attributes import InstrumentedAttribute

from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QMessageBox, QDialog, QHBoxLayout, QWidget
import sip
from sqlalchemy import Integer, String, Text, Boolean, Float

from DBHelper.db import *
from Enums import BasePropertyType, LearningApproach, SkillTarget, SkillType, SkillLevel, \
    AdditionalPropertyType, StatusType, AchievementPropertyType, AchievementType, \
    ExpBookType, DataType, PropertyAvailability, StuffType
from qt_utils import EditWidgetType, set_geo, StatuesWidgets, PropertyWidgets, \
    TableItems, ColumnEdit, TableItem, DropStuffWidgets
from qt_utils import MyMultiLineText, MyLineText, MyLabel, MyFrame, MyComboBox, MyListBox, MyButton, MyDateTimeBox
from DBHelper.tables.base_table import CustomColumn, Timestamp, MultiLineText
from DBHelper.tables.base_table import Basic, Entity


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        print('__init__')

        self.right_region_width = 1200  # 右边区域的宽度
        self.bottom_region_height = 60  # 底部区域的高度
        self.item_height = 35  # 每个条目的宽度

        self.label_width = 120  #
        self.combo_box_width = 200  # 具体属性名字展示
        self.long_label_width = 250  # 具体属性名字展示

        self.short_text_width = 100  # 具体属性名字输入
        self.long_text_width = 400  # 具体属性名字输入

        self.right_top_region_height = 250
        self.right_middle_region_height = 250

        self.left_right_region_height = self.right_top_region_height + self.right_middle_region_height + self.right_middle_region_height
        self.left_region_width = self.label_width + self.combo_box_width

        self.button_width = 150
        self.button_top_margin = 10

        self.property_list_width = 150
        self.statues_list_width = 160
        self.interval = 5

        self.max_property_num = 6
        self.max_decompose_num = 6
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
        self.table_item: TableItem = None

        # 显示表中所有数据
        self.recordsListWidget = MyListBox()

        # 显示属性
        self.properties_widgets_list: List[PropertyWidgets] = []  # 包含index_label,name_text,value_text,
        self.all_property_list_widget = MyListBox()

        # 显示掉落物品
        self.stuff_widgets_list: List[DropStuffWidgets] = []
        self.all_stuff_list_widget = MyListBox()

        # 所有条目
        self.records: List[Entity] = []
        self.column_edit_dict: Dict[str, ColumnEdit] = dict()

        # 设置区域
        self.delButton = MyButton(text='删除选中')
        self.saveButton = MyButton(text='保存')

        self.new_name_label = MyLabel()
        self.new_name_text = MyLineText()
        self.add_entry_button = MyButton(text="新增")

        self.current_property_index = 0
        self.current_stuff_widget_index = 0

        self.initUI()

    def initUI(self):
        print('init UI')

        left_right_region_width = self.left_region_width + self.right_region_width

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
                width=self.right_region_width,
                height=self.left_right_region_height)

        # 右上
        set_geo(cur_widget=self.right_top_region,
                parent_widget=self.right_region,
                x1=0,
                y1=0,
                width=self.right_region_width,
                height=self.right_top_region_height)
        # 右中
        set_geo(cur_widget=self.right_middle_region,
                parent_widget=self.right_region,
                x1=0,
                y1=self.right_top_region_height,
                width=self.right_region_width,
                height=self.right_middle_region_height)
        # 右下
        set_geo(cur_widget=self.right_bottom_region,
                parent_widget=self.right_region,
                x1=0,
                y1=self.right_top_region_height + self.right_middle_region_height,
                width=self.right_region_width, height=self.right_top_region_height)
        # 下方
        set_geo(cur_widget=self.bottom_region,
                parent_widget=self,
                x1=0,
                y1=self.left_right_region_height,
                width=left_right_region_width,
                height=self.bottom_region_height,
                )
        # 所有项目都会加载的列表框
        self.init_property_widgets(parent=self.right_middle_region)
        self.init_open_decompose_widgets(parent=self.right_bottom_region)
        self.init_records_list_box()
        self.init_select_current_table()
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
                x1=self.current_data_table_label.right(),
                y1=0,
                width=self.combo_box_width,
                height=self.item_height)
        for table_item in TableItems.item_list.get_items():
            self.current_data_table_combo_box.addItem(table_item.name)

        self.current_data_table_combo_box.set_text(text=TableItems.default.name)
        self.current_data_table_combo_box.currentIndexChanged.connect(self.handle_data_table_select_changed)

        self.handle_data_table_select_changed(self.current_data_table_combo_box.currentIndex())

    def init_records_list_box(self):
        self.recordsListWidget = MyListBox()
        set_geo(cur_widget=self.recordsListWidget,
                parent_widget=self.left_region,
                x1=0,
                y1=self.item_height,
                width=self.left_region_width,
                height=self.left_right_region_height - self.item_height)
        self.recordsListWidget.currentItemChanged.connect(self.record_changed_event)

    def show_all_records(self):
        current_text = self.current_data_table_combo_box.currentText()
        table_class = TableItems.item_list.get_by_name(name=current_text).table_class

        if self.table_item.is_entity:
            item_names = [entity.name for entity in table_class.get_all()]
        else:
            item_names = [str(entity.id) for entity in table_class.get_all()]

        self.recordsListWidget.clear()
        self.recordsListWidget.addItems(item_names)
        if len(item_names) > 0:
            last_row = self.recordsListWidget.count() - 1
            self.recordsListWidget.item(last_row).setSelected(True)

    def handle_data_table_select_changed(self, index: int):
        print('handle_data_table_select_changed', index)
        self.clear_column_edit_widgets()

        current_text = self.current_data_table_combo_box.currentText()
        self.table_item = TableItems.item_list.get_by_name(name=current_text)

        # 判断是否有name字段
        if issubclass(self.table_item.table_class, Entity):
            self.table_item.is_entity = True
        elif issubclass(self.table_item.table_class, Basic):
            self.table_item.is_entity = False
        else:
            raise ValueError(f"当前不应该有其他类型的表。当前表名: {self.table_item.table_class}")

        print(f"table_item {self.table_item.table_class} is_entity? {self.table_item.is_entity}")

        # 编辑表属性
        columns = inspect.getmembers(self.table_item.table_class)  # 为属性增加索引，这样编辑的顺序可以固定
        self.column_edit_dict.clear()
        for column in columns:
            key = column[0]
            one_column: CustomColumn = getattr(self.table_item.table_class, key)
            if not isinstance(one_column, InstrumentedAttribute):
                continue

            editable = True
            if key == "id":
                editable = False
            if key.startswith('_'):
                print(f"key starts with {key}")
                continue

            if isinstance(one_column.type, Boolean):
                data_type = DataType.BOOL
                edit_type = EditWidgetType.bool_combo_box
            elif isinstance(one_column.type, Timestamp):
                data_type = DataType.TIMESTAMP
                edit_type = EditWidgetType.date_time_box
            elif isinstance(one_column.type, Integer):
                data_type = DataType.INTEGER
                edit_type = EditWidgetType.short_text
            elif isinstance(one_column.type, MultiLineText):
                data_type = DataType.MULTI_LINE_TEXT
                edit_type = EditWidgetType.multiline_text_box
            elif isinstance(one_column.type, Text):
                data_type = DataType.TEXT
                edit_type = EditWidgetType.long_text
            elif isinstance(one_column.type, String):
                data_type = DataType.STRING
                edit_type = EditWidgetType.short_text
            else:
                raise ValueError("还没有实现")

            if one_column.default is None:
                names = None
                default = None
            else:
                names = one_column.default.arg
                default = one_column.default.arg

            if one_column.bind_type is not None:
                edit_type = EditWidgetType.combo_box
                names = one_column.bind_type.item_list.get_names()
            elif one_column.bind_table is not None:
                edit_type = EditWidgetType.combo_box
                records = globals()[one_column.bind_table].get_all()
                names = [record.name for record in records]

            new_column_edit = ColumnEdit(
                data_type=data_type,
                key=key,
                cn=one_column.cn,
                edit_widget_type=edit_type,
                bind_type=one_column.bind_type,
                bind_table=one_column.bind_table,
                choices=names,
                editable=editable,
                default=default)

            self.column_edit_dict[key] = new_column_edit

        self.show_all_records()
        self.init_item_setting_ui()
        self.update()
        self.repaint()
        self.handle_show_widgets()

    def handle_show_widgets(self):

        # 新名称按钮等
        visible = self.table_item.is_entity
        self.new_name_label.setVisible(visible)
        self.new_name_text.setVisible(visible)

        # 编辑字段
        visible = self.recordsListWidget.currentItem() is not None

        for key in self.column_edit_dict:
            self.column_edit_dict[key].edit_widget.setVisible(visible)
            self.column_edit_dict[key].edit_label.setVisible(visible)

        # 表对应的属性
        visible = self.table_item.addition_source_type is not None and self.recordsListWidget.currentItem() is not None

        for property_widgets in self.properties_widgets_list:
            property_widgets.index_label.setVisible(visible)
            property_widgets.name_label.setVisible(visible)
            property_widgets.value_text.setVisible(visible)
            property_widgets.name_input_text.setVisible(visible)
            property_widgets.availability_label.setVisible(visible)
            property_widgets.availability_combo_box.setVisible(visible)
        self.all_property_list_widget.setVisible(visible)

        # 表对应的掉落物品
        visible = self.table_item.bind_stuff_type is not None and self.recordsListWidget.currentItem() is not None
        for drop_widgets in self.stuff_widgets_list:
            drop_widgets.index_label.setVisible(visible)
            drop_widgets.name_input_text.setVisible(visible)
            drop_widgets.name_label.setVisible(visible)

            drop_widgets.stuff_type_label.setVisible(visible)
            drop_widgets.stuff_type_combo_box.setVisible(visible)

            drop_widgets.prob_label.setVisible(visible)
            drop_widgets.prob_value_text.setVisible(visible)
        self.all_stuff_list_widget.setVisible(visible)

    def init_property_widgets(self, *, parent: QWidget):
        print("init_property_widgets")
        # 创建显示属性的文本框和按钮
        ##################################################################################
        print("init_property_list")
        set_geo(cur_widget=self.all_property_list_widget,
                parent_widget=parent,
                x1=self.label_width + self.short_text_width + self.interval,
                y1=0,
                width=self.property_list_width,
                height=self.right_middle_region_height)
        # 定义事件：
        self.all_property_list_widget.currentItemChanged.connect(self.handle_property_list_select_changed)
        self.handle_property_input_change(index=0, text="")
        self.all_property_list_widget.hide()
        ##################################################################################

        for index in range(self.max_property_num):
            index_label = MyLabel(f'属性：{index + 1}')  # 显示属性索引
            name_input_text = MyLineText(index=index)  # 输入属性名称
            # -------------------------------------
            availability_label = MyLabel()  # 作用域标签
            availability_combo_box = MyComboBox()  # 作用域选择框
            # -------------------------------------
            name_label = MyLabel()  # 属性名称标签
            value_text = MyLineText(index=index)  # 属性值

            # 定义位置大小
            set_geo(cur_widget=index_label,
                    parent_widget=parent,
                    x1=self.interval * 1,
                    y1=self.item_height * index,
                    width=self.label_width,
                    height=self.item_height)
            set_geo(cur_widget=name_input_text,
                    parent_widget=parent,
                    x1=index_label.right() + self.interval,
                    y1=self.item_height * index,
                    width=self.short_text_width,
                    height=self.item_height)

            set_geo(cur_widget=availability_label,
                    parent_widget=parent,
                    x1=self.all_property_list_widget.right() + self.interval,
                    y1=self.item_height * index,
                    width=self.label_width,
                    height=self.item_height,
                    )

            set_geo(cur_widget=availability_combo_box,
                    parent_widget=parent,
                    x1=availability_label.right() + self.interval,
                    y1=self.item_height * index,
                    width=self.combo_box_width,
                    height=self.item_height,
                    )

            set_geo(cur_widget=name_label,
                    parent_widget=parent,
                    x1=availability_combo_box.right() + self.interval,
                    y1=self.item_height * index,
                    width=self.label_width,
                    height=self.item_height)

            set_geo(cur_widget=value_text,
                    parent_widget=parent,
                    x1=name_label.right() + self.interval,
                    y1=self.item_height * index,
                    width=self.label_width,
                    height=self.item_height)
            # 设置内容
            availability_label.set_text(text="作用域")
            availability_combo_box.addItems(PropertyAvailability.item_list.get_names())
            availability_combo_box.setCurrentText(PropertyAvailability.default.name)
            # 定义事件
            name_input_text.focus.connect(self.handle_property_text_focus)
            name_input_text.focus.connect(self.handle_property_input_change)
            name_input_text.text_change.connect(self.handle_property_input_change)

            value_text.text_change.connect(self.handle_property_text_focus)

            self.properties_widgets_list.append(
                PropertyWidgets(index_label=index_label,
                                property_input_text=name_input_text,
                                availability_label=availability_label,
                                availability_combo_box=availability_combo_box,
                                name_label=name_label,
                                value_text=value_text)
            )
            index_label.hide()
            name_input_text.hide()
            availability_label.hide()
            availability_combo_box.hide()
            name_label.hide()
            value_text.hide()

    def init_open_decompose_widgets(self, *, parent: QWidget):
        print("init_open_decompose_widgets")
        # 创建显示属性的文本框和按钮
        ##################################################################################
        print("all_stuff_list_widget")
        set_geo(cur_widget=self.all_stuff_list_widget,
                parent_widget=parent,
                x1=self.label_width * 2 + self.short_text_width + self.combo_box_width + self.interval * 5,
                y1=0,
                width=self.property_list_width,
                height=self.right_middle_region_height)
        # 定义事件：
        self.all_stuff_list_widget.currentItemChanged.connect(self.handle_stuff_list_select_changed)
        self.all_stuff_list_widget.hide()
        ##################################################################################

        for index in range(self.max_decompose_num):
            index_label = MyLabel(f'掉落物品{index + 1}')  # 显示掉落物品的索引
            name_input_text = MyLineText(index=index)  # 输入物品名称
            # -------------------------------------
            stuff_type_label = MyLabel()  # 物品类型标签
            stuff_type_combo_box = MyComboBox()  # 物品类型选择框

            name_label = MyLabel()  # 物品名称
            # -------------------------------------
            prob_label = MyLabel()  # 概率标签
            prob_value_text = MyLineText(index=index)  # 概率值，1000表示100%

            # 定义位置大小
            set_geo(cur_widget=index_label,
                    parent_widget=parent,
                    x1=self.interval,
                    y1=self.item_height * index,
                    width=self.label_width,
                    height=self.item_height)

            set_geo(cur_widget=stuff_type_label,
                    parent_widget=parent,
                    x1=index_label.right() + self.interval,
                    y1=self.item_height * index,
                    width=self.label_width,
                    height=self.item_height,
                    )

            set_geo(cur_widget=stuff_type_combo_box,
                    parent_widget=parent,
                    x1=stuff_type_label.right() + self.interval,
                    y1=self.item_height * index,
                    width=self.combo_box_width,
                    height=self.item_height,
                    )

            set_geo(cur_widget=name_input_text,
                    parent_widget=parent,
                    x1=stuff_type_combo_box.right() + self.interval,
                    y1=self.item_height * index,
                    width=self.short_text_width,
                    height=self.item_height)

            set_geo(cur_widget=name_label,
                    parent_widget=parent,
                    x1=self.all_stuff_list_widget.right() + self.interval,
                    y1=self.item_height * index,
                    width=self.short_text_width,
                    height=self.item_height)

            set_geo(cur_widget=prob_label,
                    parent_widget=parent,
                    x1=name_label.right() + self.interval,
                    y1=self.item_height * index,
                    width=self.short_text_width,
                    height=self.item_height)

            set_geo(cur_widget=prob_value_text,
                    parent_widget=parent,
                    x1=prob_label.right() + self.interval,
                    y1=self.item_height * index,
                    width=self.label_width,
                    height=self.item_height)

            # 设置内容
            stuff_type_label.set_text(text="物品类型")
            stuff_type_combo_box.addItems(StuffType.item_list.get_names())
            stuff_type_combo_box.setCurrentText(StuffType.default.name)
            stuff_type_combo_box.currentTextChanged.connect(self.handle_change_stuff_type)

            prob_label.set_text(text='概率')
            # 定义事件
            name_input_text.focus.connect(self.handle_stuff_input_text_focus)
            name_input_text.focus.connect(self.handle_change_drop_stuffs_list)
            name_input_text.text_change.connect(self.handle_change_drop_stuffs_list)


            self.stuff_widgets_list.append(
                DropStuffWidgets(index_label=index_label,
                                 name_input_text=name_input_text,
                                 stuff_type_label=stuff_type_label,
                                 stuff_type_combo_box=stuff_type_combo_box,
                                 name_label=name_label,
                                 prob_label=prob_label,
                                 prob_value_text=prob_value_text)
            )
            # self.handle_change_stuff_type(StuffType.default.name)  # 初始加载的时候算作选择了第一个物品类型选项
            index_label.hide()
            name_input_text.hide()
            stuff_type_label.hide()
            stuff_type_combo_box.hide()
            name_label.hide()
            prob_label.hide()
            prob_value_text.hide()

    def init_bottom_widgets(self):
        print("init_bottom_widgets")

        # 删除按钮
        set_geo(cur_widget=self.delButton,
                parent_widget=self.bottom_region,
                x1=self.interval,
                y1=self.button_top_margin,
                width=self.button_width,
                height=self.item_height)

        # 新增 技能文本框，按钮
        set_geo(cur_widget=self.new_name_label,
                parent_widget=self.bottom_region,
                x1=self.delButton.right() + self.interval * 10 + self.interval,
                y1=self.button_top_margin,
                width=self.button_width,
                height=self.item_height
                )
        self.new_name_label.setText('新名称')

        set_geo(cur_widget=self.new_name_text,
                parent_widget=self.bottom_region,
                x1=self.new_name_label.right() + self.interval,
                y1=self.button_top_margin,
                width=self.long_text_width,
                height=self.item_height
                )
        set_geo(cur_widget=self.add_entry_button,
                parent_widget=self.bottom_region,
                x1=self.new_name_text.right() + self.interval,
                y1=self.button_top_margin,
                width=self.button_width,
                height=self.item_height
                )

        # 保存按钮
        set_geo(cur_widget=self.saveButton,
                parent_widget=self.bottom_region,
                x1=self.add_entry_button.right() + self.interval,
                y1=self.button_top_margin,
                width=self.button_width,
                height=self.item_height)
        # 定义事件
        self.delButton.clicked.connect(self.handle_del_record)
        self.add_entry_button.clicked.connect(self.handle_add_record)
        self.saveButton.clicked.connect(self.handle_save_record)

    #
    # def init_status_list(self):
    #     print("init_status_list")
    #     # 创建显示附加属性的显示列表
    #     for index in range(4):
    #         statues_index_label = MyLabel(f'状态：{index + 1}')
    #         statues_name_text = MyLineText(index=index)
    #         # -------------------------------------
    #         statues_name_label = MyLabel()
    #
    #         # 定义位置大小
    #         set_geo(cur_widget=statues_index_label,
    #                 parent_widget=self.right_bottom_region,
    #                 x1=self.interval * 1,
    #                 y1=self.item_height * index,
    #                 width=self.label_width,
    #                 height=self.item_height)
    #         set_geo(cur_widget=statues_name_text,
    #                 parent_widget=self.right_bottom_region,
    #                 x1=self.label_width + self.interval * 2,
    #                 y1=self.item_height * index,
    #                 width=self.short_text_width,
    #                 height=self.item_height)
    #         set_geo(cur_widget=statues_name_label,
    #                 parent_widget=self.right_bottom_region,
    #                 x1=self.label_width + self.short_text_width + self.statues_list_width + self.interval * 4,
    #                 y1=self.item_height * index,
    #                 width=self.long_label_width,
    #                 height=self.item_height)
    #
    #         # 定义事件
    #         statues_name_text.focus.connect(self.handle_property_text_focus)
    #         statues_name_text.text_change.connect(self.handle_property_input_change)
    #
    #         self.properties_widgets_list.append(
    #             StatuesWidgets(statues_index_label=statues_index_label,
    #                            statues_name_text=statues_name_text,
    #                            statues_name_label=statues_name_label,
    #                            )
    #         )

    def clear_column_edit_widgets(self):
        print("clear_column_edit_widgets")
        self.column_edit_dict.clear()
        for item in self.right_top_region.children():
            sip.delete(item)

    def init_item_setting_ui(self):
        print("init_item_setting_ui")
        widget_index = -1
        for key in self.column_edit_dict:
            widget_index += 1
            edit_item = self.column_edit_dict[key]

            label_x1 = self.interval
            label_y1 = widget_index * self.item_height

            edit_x1 = self.label_width + self.interval
            edit_y1 = label_y1

            # label
            label = MyLabel(label_text=edit_item.cn)
            set_geo(cur_widget=label,
                    parent_widget=self.right_top_region,
                    x1=label_x1,
                    y1=label_y1,
                    width=self.label_width,
                    height=self.item_height)
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
            elif edit_item.edit_widget_type in (EditWidgetType.multiline_text_box,):
                edit_widget = MyMultiLineText()
                set_geo(cur_widget=edit_widget,
                        parent_widget=self.right_top_region,
                        x1=edit_x1,
                        y1=edit_y1,
                        width=self.long_text_width,
                        height=self.item_height * 3)
                edit_widget.set_text(text=edit_item.choices)
                widget_index += 2

            elif edit_item.edit_widget_type in (EditWidgetType.long_text,):
                edit_widget = MyLineText()
                set_geo(cur_widget=edit_widget,
                        parent_widget=self.right_top_region,
                        x1=edit_x1,
                        y1=edit_y1,
                        width=self.long_text_width,
                        height=self.item_height)
                edit_widget.set_text(text=edit_item.choices)

            elif edit_item.edit_widget_type in (EditWidgetType.date_time_box,):
                edit_widget = MyDateTimeBox()
                set_geo(cur_widget=edit_widget,
                        parent_widget=self.right_top_region,
                        x1=edit_x1,
                        y1=edit_y1,
                        width=self.long_text_width,
                        height=self.item_height)
                # todo:?

            elif edit_item.edit_widget_type in (EditWidgetType.combo_box,):
                edit_widget = MyComboBox()
                edit_widget.addItems(edit_item.choices)
                edit_widget.set_text(text=edit_item.default)
                set_geo(cur_widget=edit_widget,
                        parent_widget=self.right_top_region,
                        x1=edit_x1,
                        y1=edit_y1,
                        width=self.combo_box_width,
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

            if not edit_item.editable:
                edit_widget.setEnabled(False)
            self.column_edit_dict[edit_item.key].edit_widget = edit_widget
            self.column_edit_dict[edit_item.key].edit_label = label

    def handle_add_record(self):
        print("handle_add_record")

        if self.table_item.is_entity:
            new_name = self.new_name_text.text()
            if new_name == "":
                QMessageBox.information(self, '出错了！', '名称不可为空')
                return
            if Achievement.is_exists_by_name(name=new_name):
                QMessageBox.information(self, '出错了！', '成就已经存在了')
                return
            self.table_item.table_class.add_or_update_by_name(name=new_name)
            self.new_name_text.clear()
        else:
            self.table_item.table_class.add_with_kwargs(kwargs=dict())
        self.show_all_records()

    def handle_property_text_focus(self, index: int, text: str):
        print("handle_property_text_focus")
        self.current_property_index = index
        print(f'cur properties index is {self.current_property_index}')

    def handle_stuff_input_text_focus(self, index: int, text: str):
        print("handle_stuff_input_text_focus")
        self.current_stuff_widget_index = index
        print(f'cur current_stuff_widget_index index is {self.current_stuff_widget_index}')

    def handle_property_input_change(self, index: int, text: str):
        print('handle_property_input_change')
        self.all_property_list_widget.clear()

        for property_name in AdditionalPropertyType.item_list.name_dict:
            if text not in property_name:
                continue
            self.all_property_list_widget.addItem(property_name)

        # 如果属性列表的属性个数大于0并且已经加载完毕属性列表；
        if self.all_property_list_widget.count() != 0 and len(self.properties_widgets_list) > 0:
            if self.properties_widgets_list[self.current_property_index].name_label.text() == "":
                first_item = self.all_property_list_widget.item(0)
                self.properties_widgets_list[self.current_property_index].name_label.set_text(text=first_item.text())

    def handle_change_drop_stuffs_list(self, index: int, text: str):
        print('handle_change_drop_stuffs_list')
        self.all_stuff_list_widget.clear()

        current_stuff_type_name = self.stuff_widgets_list[self.current_stuff_widget_index].stuff_type_combo_box.text()
        bind_table = StuffType.item_list.get_by_name(name=current_stuff_type_name).bind_table
        all_records = globals()[bind_table].get_all()
        for record in all_records:
            if text in record.name:
                self.all_stuff_list_widget.addItem(record.name)

        # 如果属性列表的属性个数大于0并且已经加载完毕属性列表；
        # if self.all_stuff_list_widget.count() != 0 and len(self.stuff_widgets_list) > 0:
        #     if self.stuff_widgets_list[self.current_stuff_widget_index].name_input_text.text() == "":
        #         first_item = self.all_stuff_list_widget.item(0)
        #         self.stuff_widgets_list[self.current_stuff_widget_index].name_input_text.set_text(
        #             text=first_item.text())

    def handle_change_stuff_type(self, text: str):
        self.all_stuff_list_widget.clear()

        bind_table = StuffType.item_list.get_by_name(name=text).bind_table
        all_stuffs = globals()[bind_table].get_all()
        self.stuff_widgets_list[self.current_stuff_widget_index].name_input_text.set_text(text='')
        self.all_stuff_list_widget.addItems([stuff.name for stuff in all_stuffs])

    def handle_property_list_select_changed(self, ):
        """
        用户点击了属性列表
        :return:
        """
        print("handle_property_list_select_changed")
        if not self.all_property_list_widget.text():
            return
        property_name = self.all_property_list_widget.text()
        self.properties_widgets_list[self.current_property_index].name_label.set_text(text=property_name)

    def clear_properties(self):
        for properties_widget in self.properties_widgets_list:
            properties_widget.name_input_text.set_text(text="")
            properties_widget.name_label.set_text(text="")
            properties_widget.value_text.set_text(text="")
            properties_widget.availability_combo_box.set_text(text=PropertyAvailability.default.name)

    def clear_stuffs(self):
        for stuff_widgets in self.stuff_widgets_list:
            stuff_widgets.name_input_text.set_text(text="")
            stuff_widgets.stuff_type_label.set_text(text="")
            stuff_widgets.prob_value_text.set_text(text="")
            stuff_widgets.stuff_type_combo_box.set_text(text=StuffType.default.name)

    def handle_stuff_list_select_changed(self, ):
        """
        用户点击了属性列表
        :return:
        """
        print("handle_stuff_list_select_changed")
        if not self.all_stuff_list_widget.text():
            return
        stuff_name = self.all_stuff_list_widget.text()
        self.stuff_widgets_list[self.current_stuff_widget_index].name_label.set_text(text=stuff_name)

    def record_changed_event(self, item):
        if not item:
            print(f"item is {item}")
            return
        if self.table_item.table_class is None:
            print("self.cur_table is None")
            return
        record_name_or_id = item.text()

        if self.table_item.is_entity:
            record = self.table_item.table_class.get_by_name(name=record_name_or_id)
        else:
            record = self.table_item.table_class.get_by_id(_id=int(record_name_or_id))

        for key in self.column_edit_dict:
            value = getattr(record, key)
            edit_item = self.column_edit_dict[key]
            if value is None:
                ...
            elif edit_item.bind_type is not None:
                value = edit_item.bind_type.item_list.get_by_index(index=value).name
            elif edit_item.bind_table is not None:
                value = globals()[edit_item.bind_table].get_by_id(_id=value).name
            else:
                ...
            self.column_edit_dict[key].edit_widget.set_text(text=value)

        if self.table_item.addition_source_type is not None:
            properties = MiscProperties.get_properties_by(
                additional_source_type=self.table_item.addition_source_type.index,
                additional_source_id=record.id
            )
            self.show_properties(properties=properties)
        if self.table_item.bind_stuff_type is not None:
            stuffs = OpenDecomposeOrDropStuffsRecord.get_all_by(source_type=self.table_item.bind_stuff_type.index,
                                                                source_id=record.id,
                                                                )
            self.show_drop_stuffs(stuffs=stuffs)
        self.handle_show_widgets()

    def show_properties(self, *, properties: List[MiscProperties]):
        self.clear_properties()
        for status_property in properties:
            property_name = AdditionalPropertyType.item_list.get_by_index(
                index=status_property.additional_property_type
            ).name
            property_index = status_property.additional_source_property_index
            self.properties_widgets_list[property_index].name_input_text.set_text(text=property_name)
            self.properties_widgets_list[property_index].name_label.set_text(text=property_name)
            self.properties_widgets_list[property_index].value_text.set_text(
                text=status_property.additional_property_value)

    def show_drop_stuffs(self, *, stuffs: List[OpenDecomposeOrDropStuffsRecord]):
        self.clear_stuffs()
        for drop_stuff in stuffs:
            stuff_type_name = StuffType.item_list.get_by_index(
                index=drop_stuff.acquire_stuff_type
            ).name

            bind_table = StuffType.item_list.get_by_name(name=stuff_type_name).bind_table
            explicit_stuff = globals()[bind_table].get_by_id(_id=drop_stuff.acquire_stuff_id)  # 具体的，比如某个装备

            self.stuff_widgets_list[drop_stuff.acquire_stuff_index].name_input_text.set_text(text=explicit_stuff.name)
            self.stuff_widgets_list[drop_stuff.acquire_stuff_index].name_label.set_text(text=explicit_stuff.name)
            self.stuff_widgets_list[drop_stuff.acquire_stuff_index].stuff_type_combo_box.set_text(text=stuff_type_name)
            self.stuff_widgets_list[drop_stuff.acquire_stuff_index].prob_value_text.set_text(
                text=drop_stuff.acquire_stuff_prob)


    def handle_del_record(self):
        """
        删除当前选中的记录
        """
        current_record_name_or_id = self.recordsListWidget.text()
        if self.recordsListWidget.currentItem() is None:
            QMessageBox.information(self, "错误", "没有选中任何记录")
            return
        reply = QMessageBox.question(self, '退出', f'确定删除{current_record_name_or_id}？',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.No:
            return

        if self.table_item.is_entity:
            self.table_item.table_class.del_by_name(name=current_record_name_or_id)
        else:
            current_record_name_or_id = int(current_record_name_or_id)
            self.table_item.table_class.del_by_id(_id=current_record_name_or_id)
        print(f"删除name 或者 id 为 {current_record_name_or_id} 的记录成功！")
        self.show_all_records()

    def handle_save_record(self):
        print("handle_save_record")

        record_name_or_id = self.recordsListWidget.text()
        if self.recordsListWidget.currentItem() is None:
            QMessageBox.information(self, "错误", "没有选中任何记录")
            return
        if self.table_item.is_entity:
            record: Entity = self.table_item.table_class.get_by_name(name=record_name_or_id)
        else:
            record: Basic = self.table_item.table_class.get_by_id(_id=record_name_or_id)

        update_args = dict()
        for key in self.column_edit_dict:
            column_edit: ColumnEdit = self.column_edit_dict[key]
            value = column_edit.edit_widget.text()

            if column_edit.bind_type is not None:
                value = column_edit.bind_type.item_list.get_by_name(name=value).index
            elif column_edit.bind_table is not None:
                value = globals()[column_edit.bind_table].get_by_name(name=value).id

            if column_edit.data_type == DataType.INTEGER:
                if value == "":
                    value = None
                else:
                    value = int(value)
            elif column_edit.data_type in (DataType.STRING, DataType.MULTI_LINE_TEXT, DataType.TEXT):
                ...
            elif column_edit.data_type == DataType.BOOL:
                if value == "True":
                    value = True
                elif value == "False":
                    value = False
                else:
                    raise ValueError("不支持的类型")
            else:
                raise ValueError("不支持的类型")
            update_args[key] = value

        record.update_kwargs_by_id(_id=record.id, kwargs=update_args)
        self.show_all_records()

        # 对表格对应的属性进行操作；
        ########################################################
        current_table_name = self.current_data_table_combo_box.currentText()
        self.table_item = TableItems.item_list.get_by_name(name=current_table_name)
        if self.table_item.addition_source_type is not None:
            # 删除对应属性
            MiscProperties.del_by_additional_source_type_id(
                additional_source_type=self.table_item.addition_source_type.index,
                additional_source_id=record.id,
            )
            for index, properties_widget in enumerate(self.properties_widgets_list):
                # 属性类型
                property_cn_name = properties_widget.name_label.text()
                if property_cn_name == "":
                    continue
                property_type_index = AdditionalPropertyType.item_list.name_dict[property_cn_name].index

                # 属性的作用域
                property_availability_cn = properties_widget.availability_combo_box.currentText()
                if property_availability_cn == "":
                    property_availability_index = None
                else:
                    property_availability_index = PropertyAvailability.item_list.get_by_name(
                        name=property_availability_cn).index

                # 属性值
                property_value_text = properties_widget.value_text.text()
                if property_value_text == "":
                    continue
                property_value = int(property_value_text)

                MiscProperties.add(
                    additional_source_type=self.table_item.addition_source_type.index,
                    additional_source_id=record.id,

                    additional_property_type=property_type_index,
                    additional_property_value=property_value,

                    additional_source_property_index=index,

                    property_availability=property_availability_index,
                )
                print(
                    f"表格名称：{current_table_name}，记录名称{record.name}，第{index + 1}条属性：{property_cn_name}=属性值{property_value} 更新成功。")
            ########################################################

        # 对应物品的掉落情况保存
        if self.table_item.bind_stuff_type is not None:
            # 删除对应物品掉落情况
            OpenDecomposeOrDropStuffsRecord.del_all_by_source_type_source_id(
                source_type=self.table_item.bind_stuff_type.index,
                source_id=record.id,
            )
            for index, stuff_widget in enumerate(self.stuff_widgets_list):
                # 属性类型
                stuff_cn_name = stuff_widget.name_label.text()
                if stuff_cn_name == "":
                    continue

                stuff_type_cn_name = self.stuff_widgets_list[index].stuff_type_combo_box.text()
                source_item = StuffType.item_list.get_by_name(name=stuff_type_cn_name)
                stuff_type_index = source_item.index
                bind_table = source_item.bind_table

                stuff = globals()[bind_table].get_by_name(name=stuff_cn_name)

                # 属性值
                stuff_prob = stuff_widget.prob_value_text.text()
                stuff_prob = int(stuff_prob)

                OpenDecomposeOrDropStuffsRecord.add(
                    source_type=StuffType.item_list.get_by_name(name=current_table_name).index,
                    source_id=record.id,
                    acquire_stuff_index=index,
                    acquire_stuff_type=stuff_type_index,
                    acquire_stuff_id=stuff.id,
                    acquire_stuff_prob=stuff_prob
                )

                print(
                    f"表格名称：{current_table_name}，记录名称{record.name}，第{index + 1}个掉落物品：{stuff_cn_name},概率值 {stuff_prob} 更新成功。")
            ########################################################


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
