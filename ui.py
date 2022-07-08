# -*- coding: utf-8 -*-
import datetime
import dearpygui.dearpygui as dpg

dpg.create_context()

today = datetime.date.today()
test_value = 'TETXT'


def button_callback(sender, app_data, user_data):
    global test_value
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")
    print(dpg.get_value(sender))
    test_value = 'JHIO'

    dpg.set_value(item='Row1 Column2', value='HUIETA')


def get_cell_value(row, column):
    return 'HUi'


def test_handle():
    dpg.set_value("Row1 Column1 text", "POIZDA")

dpg.create_viewport(title='Log Report', width=800, height=400)

with dpg.font_registry():
    with dpg.font(f'rfont.ttf', 13, default_font=True, id="Default font"):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
dpg.bind_font("Default font")

with dpg.window(label="Лог отчет по кормам", tag='Primary window', width=800, height=400):
    dpg.add_date_picker(label='Выберите дату', 
        default_value={'month_day': today.day, 'year': 100 + today.year % 2000, 'month': today.month - 1},
        callback=button_callback, user_data="Date Data")
    
    with dpg.item_handler_registry(tag="test handler") as handler:
        dpg.add_item_clicked_handler(callback=test_handle)

    dpg.add_button(label="Сформировать отчет", callback=button_callback, user_data="Button Data")

    # dpg.add_text('JJASKDK', tag='test text', pos=[300, 30])

    with dpg.table(tag='Report Table', pos=[200, 40], width=500):

        dpg.add_table_column(label="Header 1")
        dpg.add_table_column(label="Header 2")
        dpg.add_table_column(label="Header 3")

        # once it reaches the end of the columns
        for i in range(0, 4):
            with dpg.table_row():
                for j in range(0, 3):
                    with dpg.table_cell(tag=f"Row{i} Column{j}"):
                        dpg.add_text(tag=f"Row{i} Column{j} text", default_value=f"Row{i} Column{j}")
                        dpg.add_text(get_cell_value(row=i, column=j))
                        dpg.add_text(test_value)

    with dpg.item_handler_registry(tag="test handler") as handler:
        dpg.add_item_clicked_handler(callback=test_handle)

    dpg.bind_item_handler_registry("Row1 Column1 text", "test handler")

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()