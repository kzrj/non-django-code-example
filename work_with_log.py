import datetime

ROOT_SLICE = slice(0, 14)
DATE_SLICE = slice(15, 38)
COMMENT_SLICE = slice(40, -1)


class SliceIndex(object):
    def __init__(self, start_slice_index, date=None, init_slice=None):
        self.start_slice_index = start_slice_index
        self.date = date
        self.slice = slice(start_slice_index, None)

        if init_slice:
            self.slice = init_slice

    def set_slice(self, end_slice_index):
        self.slice = slice(self.start_slice_index, end_slice_index)


def create_day_log_file(date_indexes, lines):
    for date_index in date_indexes:        
        file_name = date_index.date.strftime("logs/%d-%m-%Y.log")
        with open(file_name, 'w', encoding='utf-8') as day_log_file:
            day_log_file.writelines(lines[date_index.slice])
            day_log_file.close()


def split_log_file_by_days(filename='cormoceh.log'):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        current_date = None
        date_indexes = []
        current_date_index = None

        for index, line in enumerate(lines):

            if not 'DEBUG' in line[ROOT_SLICE]:
                continue

            line_date = datetime.date.fromisoformat(line[DATE_SLICE].lstrip('[').split(' ')[0])

            if current_date != line_date:
                current_date = line_date

                if current_date_index:
                    current_date_index.set_slice(end_slice_index=index)

                current_date_index = SliceIndex(start_slice_index=index, date=current_date) 
                date_indexes.append(current_date_index)

    return date_indexes, lines


if __name__ == '__main__':
    # date_indexes, lines = split_log_file_by_days()
    # create_day_log_file(date_indexes, lines)

    with open('17-05-2022.log', 'w', encoding='utf-8') as test_file:
        test_file.write('hui')