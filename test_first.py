import datetime
import work_with_log as wwl


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


# def test_create_day_log_file():
#     lines, date_indexes = ['1','2','3','4'], \
#         (wwl.DateIndex(date_index=0, date=datetime.date(2022, 6, 30), init_slice=slice(0,2)),
#          wwl.DateIndex(date_index=2, date=datetime.date(2022, 7, 1),))
#     wwl.create_day_log_file(lines, date_indexes)


