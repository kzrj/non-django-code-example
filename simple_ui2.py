import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date

from daily_log import DailySession
import work_with_log as wwl


def is_it_today(target_date, filename='cormoceh.log'):
    if date.today() == target_date:
        date_indexes, lines = wwl.split_log_file_by_days(filename=filename)
        wwl.create_day_log_file(date_indexes, lines)

    return target_date


class FeedReportApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Лог отчет по кормам")
        self.root.geometry("800x600")

        # Стиль для кнопок и текста
        self.font = ('Arial', 12)

        self.create_widgets()

    def create_widgets(self):
        # 1. Поля ввода даты (простой вариант)
        date_frame = ttk.Frame(self.root)
        date_frame.pack(pady=10)

        ttk.Label(date_frame, text="День:", font=self.font).pack(side=tk.LEFT)
        self.day_entry = ttk.Entry(date_frame, width=3)
        self.day_entry.pack(side=tk.LEFT, padx=5)
        self.day_entry.insert(0, str(datetime.now().day))

        ttk.Label(date_frame, text="Месяц:", font=self.font).pack(side=tk.LEFT)
        self.month_entry = ttk.Entry(date_frame, width=3)
        self.month_entry.pack(side=tk.LEFT, padx=5)
        self.month_entry.insert(0, str(datetime.now().month))

        ttk.Label(date_frame, text="Год:", font=self.font).pack(side=tk.LEFT)
        self.year_entry = ttk.Entry(date_frame, width=5)
        self.year_entry.pack(side=tk.LEFT, padx=5)
        self.year_entry.insert(0, str(datetime.now().year))

        ttk.Button(
            date_frame,
            text="Загрузить",
            command=self.update_table
        ).pack(side=tk.LEFT, padx=10)

        # 2. Таблица с данными
        self.tree = ttk.Treeview(
            self.root,
            columns=('feed', 'ordered', 'produced'),
            show='headings'
        )

        self.tree.heading('feed', text='Название корма')
        self.tree.heading('ordered', text='Заказано (кг)')
        self.tree.heading('produced', text='Произведено (кг)')

        self.tree.column('feed', width=400)
        self.tree.column('ordered', width=200, anchor=tk.CENTER)
        self.tree.column('produced', width=200, anchor=tk.CENTER)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Добавляем пустые строки
        for _ in range(20):
            self.tree.insert('', tk.END, values=('', '', ''))

        # Прокрутка
        scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def update_table(self):
        try:
            day = int(self.day_entry.get())
            month = int(self.month_entry.get())
            year = int(self.year_entry.get())

            target_date = date(year=year, month=month, day=day)
            target_date = is_it_today(target_date=target_date)

            daily_session = DailySession()
            daily_session.parse_daily_log(filename=f'logs/{target_date.strftime("%d-%m-%Y")}.log')

            # Очищаем таблицу
            for item in self.tree.get_children():
                self.tree.item(item, values=('', '', ''))

            # Заполняем данными
            for idx, batch in enumerate(daily_session.batches()):
                if idx >= 20:
                    break
                self.tree.item(
                    self.tree.get_children()[idx],
                    values=(
                        batch.receipt_name,
                        str(batch.init_count_batches),
                        str(batch.fact_batches_count)
                    )
                )

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные:\n{str(e)}")


if __name__ == '__main__':
    root = tk.Tk()
    app = FeedReportApp(root)
    root.mainloop()
