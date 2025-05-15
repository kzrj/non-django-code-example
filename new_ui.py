# -*- coding: utf-8 -*-
import datetime

from daily_log import DailySession
import work_with_log as wwl


def is_it_today(target_date, filename='cormoceh.log'):
    if datetime.date.today() == target_date:
        date_indexes, lines = wwl.split_log_file_by_days(filename=filename)
        wwl.create_day_log_file(date_indexes, lines)

    return target_date

if __name__ == '__main__':
    target_date = datetime.date(2022, 8, 26)
    # target_date = datetime.date.today()
    target_date = is_it_today(target_date)

    daily_session = DailySession()
    daily_session.parse_daily_log(filename=f'logs/{target_date.strftime("%d-%m-%Y")}.log')

    for idx, batch in enumerate(daily_session.batches()):
        print(batch.receipt_name)

    print('OK!')
