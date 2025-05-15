# -*- coding: utf-8 -*-
# from datetime import date
#
# from daily_log import DailySession
# import work_with_log as wwl
#
#
# def is_it_today(target_date, filename='cormoceh.log'):
#     # if date.today() == target_date:
#     date_indexes, lines = wwl.split_log_file_by_days(filename=filename)
#     wwl.create_day_log_file(date_indexes, lines)
#
#     return target_date


# def display_report(target_date):
#     """Выводит отчет в консоль"""
#     try:
#         daily_session = DailySession()
#         daily_session.parse_daily_log(filename=f'logs/{target_date.strftime("%d-%m-%Y")}.log')
#
#         print("\n" + "=" * 50)
#         print(f"Отчет по кормам за {target_date.strftime('%d.%m.%Y')}")
#         print("=" * 50)
#         print(f"{'Название корма':<30} | {'Заказано (кг)':>12} | {'Произведено (кг)':>15}")
#         print("-" * 65)
#
#         for batch in daily_session.batches():
#             print(f"{batch.receipt_name:<30} | {batch.init_count_batches:>12} | {batch.fact_batches_count:>15}")
#
#         print("=" * 50 + "\n")
#
#     except FileNotFoundError:
#         print(f"\nОшибка: Файл с логами за {target_date.strftime('%d.%m.%Y')} не найден")
#     except Exception as e:
#         print(f"\nОшибка: {str(e)}")


# def main():
#     print("\n" + "=" * 50)
#     print("Система отчетов по кормам (консольная версия)")
#     print("=" * 50)

    # while True:
    #     try:
    #         # Ввод даты
    #         date_str = input("\nВведите дату в формате ДД-ММ-ГГГГ (или 'q' для выхода): ")
    #
    #         if date_str.lower() == 'q':
    #             break
    #
    #         day, month, year = map(int, date_str.split('-'))
    #         target_date = date(year=year, month=month, day=day)
    #         target_date = is_it_today(target_date=target_date)
    #
    #         # Вывод отчета
    #         display_report(target_date)
    #
    #     except ValueError:
    #         print("Ошибка: Неверный формат даты. Используйте ДД-ММ-ГГГГ")
    #     except KeyboardInterrupt:
    #         print("\nЗавершение работы...")
    #         break


if __name__ == '__main__':
    # print("\n" + "=" * 50)
    print("Система отчетов по кормам (консольная версия)")
    print("=" * 50)
    # main()
