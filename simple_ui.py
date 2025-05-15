import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from tkcalendar import Calendar
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
        self.root.geometry("900x650")

        # Настройка стилей
        self.style = ttk.Style()
        self.style.configure('Treeview', font=('Arial', 11), rowheight=25)
        self.style.configure('Treeview.Heading', font=('Arial', 12, 'bold'))

        self.create_widgets()

    def create_widgets(self):
        # 1. Верхняя панель с календарем
        top_frame = ttk.Frame(self.root)
        top_frame.pack(pady=15, padx=10, fill=tk.X)

        ttk.Label(top_frame, text="Выберите дату:", font=('Arial', 12)).pack(side=tk.LEFT)

        # Календарь
        self.cal = Calendar(
            top_frame,
            selectmode='day',
            date_pattern='dd-mm-yyyy',
            font=('Arial', 12),
            background='white',
            foreground='black',
            selectbackground='#4a6baf'
        )
        self.cal.pack(side=tk.LEFT, padx=10)

        # Кнопка обновления
        ttk.Button(
            top_frame,
            text="Загрузить данные",
            command=self.update_table,
            style='Accent.TButton'
        ).pack(side=tk.LEFT, padx=10)

        # Стиль для кнопки (только для Windows 10/11)
        self.style.map('Accent.TButton', background=[('active', '#4a6baf')])

        # 2. Таблица с данными
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Создаем Treeview с вертикальной прокруткой
        self.tree = ttk.Treeview(
            table_frame,
            columns=('feed', 'ordered', 'produced'),
            show='headings',
            selectmode='browse'
        )

        # Настраиваем колонки
        self.tree.heading('feed', text='Название корма')
        self.tree.heading('ordered', text='Заказано (кг)')
        self.tree.heading('produced', text='Произведено (кг)')

        self.tree.column('feed', width=500, anchor=tk.W)
        self.tree.column('ordered', width=200, anchor=tk.CENTER)
        self.tree.column('produced', width=200, anchor=tk.CENTER)

        # Добавляем прокрутку
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Размещаем компоненты
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Заполняем таблицу пустыми строками
        for _ in range(20):
            self.tree.insert('', tk.END, values=('', '', ''))

    def update_table(self):
        # try:
            selected_date = self.cal.get_date()
            day, month, year = map(int, selected_date.split('-'))

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
                ordered = str(batch.init_count_batches)
                produced = str(batch.fact_batches_count)

                self.tree.item(
                    self.tree.get_children()[idx],
                    values=(
                        batch.receipt_name,
                        ordered,
                        produced
                    )
                )

            # messagebox.showinfo("Успех", f"Данные за {selected_date} загружены")

        # except Exception as e:
        #     messagebox.showerror("Ошибка", f"Не удалось загрузить данные:\n{str(e)}")


if __name__ == '__main__':
    root = tk.Tk()

    # Устанавливаем тему (для Windows 10/11)
    try:
        root.tk.call('source', 'sun-valley.tcl')
        root.tk.call('set_theme', 'light')
    except:
        pass

    app = FeedReportApp(root)
    root.mainloop()