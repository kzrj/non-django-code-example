# -*- coding: utf-8 -*-
import os
import sys
import ctypes

# Автоматически определяем путь к папке с программой
def fix_win7_dll_issue():
    if sys.platform == "win32":
        # Путь к папке, где лежит exe или скрипт
        base_dir = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        # Добавляем эту папку в начало PATH
        os.environ["PATH"] = base_dir + os.pathsep + os.environ["PATH"]

        for dll in ["vcruntime140.dll", "msvcp140.dll"]:
            try:
                ctypes.CDLL(os.path.join(base_dir, dll))
            except Exception as e:
                print(f"Ошибка загрузки {dll}: {e}")

fix_win7_dll_issue()  # Вызываем сразу

import datetime
import dearpygui.dearpygui as dpg

from daily_log import DailySession
import work_with_log as wwl 


def is_it_today(target_date, filename='cormoceh.log'):
    if datetime.date.today() == target_date:
        date_indexes, lines = wwl.split_log_file_by_days(filename=filename)
        wwl.create_day_log_file(date_indexes, lines)
    
    return target_date


def button_callback(sender, app_data, user_data):
    for i in range(0, 20):
        for j in range(0, 3):
            dpg.set_value(item=f'Row{i} Column{j} text', value='')

    year = 2000 + app_data['year'] % 100
    target_date = is_it_today(target_date=datetime.date(
        year=year, month=app_data['month'] + 1, day=app_data['month_day']))

    daily_session = DailySession()
    daily_session.parse_daily_log(filename=f'logs/{target_date.strftime("%d-%m-%Y")}.log')

    for idx, batch in enumerate(daily_session.batches()):
        dpg.set_value(item=f'Row{idx} Column0 text', value=batch.receipt_name)
        dpg.set_value(item=f'Row{idx} Column1 text', value=batch.init_count_batches)
        dpg.set_value(item=f'Row{idx} Column2 text', value=batch.fact_batches_count)


if __name__ == '__main__':
    dpg.create_context()

    dpg.create_viewport(title='Log Report', width=600, height=700)

    with dpg.font_registry():
        with dpg.font(f'rfont.ttf', 13, default_font=True, id="Default font"):
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
    dpg.bind_font("Default font")

    with dpg.window(label="Лог отчет по кормам", tag='Primary window', width=600, height=700):
        today=datetime.date.today()

        dpg.add_date_picker(label='Выберите дату', 
            default_value={'month_day': today.day, 'year': 100 + today.year % 2000, 'month': today.month - 1},
            callback=button_callback, user_data="Date Data")
        
        with dpg.table(tag='Report Table', pos=[200, 40], width=600):

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