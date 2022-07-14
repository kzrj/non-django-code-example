import os
import datetime
from freezegun import freeze_time

import work_with_log as wwl
from ui import is_it_today


def test_split_log_file_by_days():
    date_indexes, lines = wwl.split_log_file_by_days(filename='test_days_cormoceh.log')
    
    assert len(date_indexes) == 3
    assert len(lines) == 9

    assert date_indexes[0].date == datetime.date(2022, 5, 2)
    assert date_indexes[1].date == datetime.date(2022, 5, 4)
    assert date_indexes[2].date == datetime.date(2022, 5, 5)

    assert date_indexes[0].slice == slice(0, 3)
    assert date_indexes[1].slice == slice(3, 6)
    assert date_indexes[2].slice == slice(6, None)


def test_create_day_log_file():
    if len(os.listdir('./logs')) > 0:
        for f_name in os.listdir('./logs'):
            os.remove(f'./logs/{f_name}')

    date_indexes, lines = wwl.split_log_file_by_days(filename='test_log.log')
    wwl.create_day_log_file(date_indexes, lines)

    assert len(os.listdir('./logs')) > 0


def test_is_it_today():
    with freeze_time("2022-05-16"):
        if len(os.listdir('./logs')) > 0:
            for f_name in os.listdir('./logs'):
                os.remove(f'./logs/{f_name}')

        tomorow_date = is_it_today(target_date=datetime.date(year=2022, month=5, day=17),
            filename='test_log.log')
        assert tomorow_date == datetime.date(2022, 5, 17)
        assert len(os.listdir('./logs')) == 0

        current_date = is_it_today(target_date=datetime.date(year=2022, month=5, day=16),
            filename='test_log.log')
        assert current_date == datetime.date(2022, 5, 16)
        assert len(os.listdir('./logs')) > 0

