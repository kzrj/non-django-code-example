# -*- coding: utf-8 -*-
import datetime
import os

import work_with_log as wwl 


def handle_main_log(filename='cormoceh.log'):
    date_indexes, lines = wwl.split_log_file_by_days(filename=filename)
    wwl.create_day_log_file(date_indexes, lines)
    
    os.rename('cormoceh.log', f'{datetime.date.today().strftime("%d-%m-%Y")}_copy_cormoceh.log')


if __name__ == '__main__':
    handle_main_log()