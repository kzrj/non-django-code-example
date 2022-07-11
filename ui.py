# -*- coding: utf-8 -*-
import datetime
import dearpygui.dearpygui as dpg

from daily_log import DailySession


dpg.create_context()

today = datetime.date.today()
test_value = 'TETXT'


def button_callback(sender, app_data, user_data):
    # # print(f"sender is: {sender}")
    # print(f"app_data is: {app_data}")
    # # print(f"user_data is: {user_data}")
    # # print(dpg.get_value(sender))
    # print(app_data['year'], app_data['year'] % 100, 2000 + app_data['year'] % 100 )

    for i in range(0, 20):
        for j in range(0, 3):
            dpg.set_value(item=f'Row{i} Column{j} text', value='')

    year = 2000 + app_data['year'] % 100
    target_date = datetime.date(year=year, month=app_data['month'] + 1, day=app_data['month_day'])

    daily_session = DailySession()
    daily_session.parse_daily_log(filename=f'logs/{target_date.strftime("%d-%m-%Y")}.log')

    for idx, batch in enumerate(daily_session.batches()):
        # print(idx, batch.receipt_name, batch.init_count_batches, batch.fact_batches_count)
        dpg.set_value(item=f'Row{idx} Column0 text', value=batch.receipt_name)
        dpg.set_value(item=f'Row{idx} Column1 text', value=batch.init_count_batches)
        dpg.set_value(item=f'Row{idx} Column2 text', value=batch.fact_batches_count)


dpg.create_viewport(title='Log Report', width=800, height=400)

with dpg.font_registry():
    with dpg.font(f'rfont.ttf', 13, default_font=True, id="Default font"):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
dpg.bind_font("Default font")

with dpg.window(label="Лог отчет по кормам", tag='Primary window', width=800, height=400):
    dpg.add_date_picker(label='Выберите дату', 
        default_value={'month_day': today.day, 'year': 100 + today.year % 2000, 'month': today.month - 1},
        callback=button_callback, user_data="Date Data")
    
    with dpg.table(tag='Report Table', pos=[200, 40], width=500):

        dpg.add_table_column(label="Название корма")
        dpg.add_table_column(label="Сколько заказали")
        dpg.add_table_column(label="Сколько фактически произвели")

        for i in range(0, 20):
            with dpg.table_row():
                for j in range(0, 3):
                    with dpg.table_cell(tag=f"Row{i} Column{j}"):
                        dpg.add_text(tag=f"Row{i} Column{j} text", default_value="")


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()