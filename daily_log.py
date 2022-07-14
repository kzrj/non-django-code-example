# -*- coding: utf-8 -*-
import datetime
import re
from work_with_log import SliceIndex

ROOT_SLICE = slice(0, 14)
DATE_SLICE = slice(15, 38)
COMMENT_SLICE = slice(40, -1)

receipt_name_regex = r'\"[А-Я][а-я]+.+\"'


class DailySession(object):
    def __init__(self, *args, **kwargs):
        self.file_lines = []
        self.batch_sessions = []

    def set_file_lines(self, file_lines):
        self.file_lines = file_lines

    def add_batch_sessions(self, batch_session):
        self.batch_sessions.append(batch_session)

    def fill_batches(self):
        for batch_session in self.batch_sessions:
            batch_session.handle_lines(lines=self.file_lines)
            
    def batches(self):
        return [batch for batch in self.batch_sessions if batch.receipt_name]

    def parse_daily_log(self, filename='logs/14-06-2022.log'):
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            self.file_lines = lines
            current_batch_session = None

            for line_index, line in enumerate(lines):
                if '========================S T A R T===================================' in line[COMMENT_SLICE]:
                    if current_batch_session:
                        current_batch_session.set_slice(end_slice_index=line_index)

                    line_date = datetime.datetime.strptime(line[DATE_SLICE].lstrip('[').split(',')[0], '%Y-%m-%d %H:%M:%S')
                    current_batch_session = BatchSession(start_slice_index=line_index, date=line_date)
                    self.add_batch_sessions(current_batch_session)

        self.fill_batches()


class BatchSession(SliceIndex):
    def __init__(self, *args, **kwargs):
        super(BatchSession, self).__init__(*args, **kwargs)
        self.init_count_batches = 0
        self.receipt_name = None
        self.fact_batches_list = []

    def catch_init_count(self, line):
        if 'Установка значения счетчика замесов count = ' in line:
            self.init_count_batches = line.split('=')[1].strip()

    def catch_receipt_name(self, line):
        if 'Полученный nrec рецепта' in line:
            self.receipt_name = re.findall(receipt_name_regex, line[COMMENT_SLICE])[0].strip('"')

    def catch_marker_weight2(self, line):
        if 'Загрузка весов2' in line:
            self.fact_batches_list.append(line[COMMENT_SLICE])

    def handle_lines(self, lines):
        for line in lines[self.slice]:
            self.catch_init_count(line)
            self.catch_receipt_name(line)
            self.catch_marker_weight2(line)

    @property
    def fact_batches_count(self):
        return len(self.fact_batches_list)


if __name__ == '__main__':
    daily_session = DailySession()
    daily_session.parse_daily_log()
