from Grammar.filling import *
from Grammar.dop_functions import *
from Grammar.fill_dates import *
from Grammar.fill_numbers import *

print(permission_perform_action())


#Скрипт для тестирования функции lists_words с записью ошибок
# import json
# import linecache
# import traceback
# from datetime import datetime


# def _exception_origin(exc: BaseException) -> dict:
#     """
#     Место, где исключение возникло (самый глубокий фрейм стека).
#     Возвращает имя функции, файл, номер строки и текст строки исходника.
#     """
#     tb = exc.__traceback__
#     if tb is None:
#         return {}
#     while tb.tb_next:
#         tb = tb.tb_next
#     frame = tb.tb_frame
#     co = frame.f_code
#     path = co.co_filename
#     lineno = tb.tb_lineno
#     line_text = linecache.getline(path, lineno).strip()
#     return {
#         "origin_function": co.co_name,
#         "origin_file": path,
#         "origin_line": lineno,
#         "origin_code": line_text,
#     }


# def test_lists_words(iterations):
#     """
#     Тестирует функцию lists_words заданное количество раз и записывает ошибки в errors.json
#     """
#     errors = []
    
#     for i in range(iterations):
#         try:
#             result = lists_words()
#             # Проверяем, что функция вернула результат
#             if result is None:
#                 errors.append({
#                     'iteration': i + 1,
#                     'error_type': 'NoneResult',
#                     'error_message': 'Функция вернула None',
#                     'tested_function': 'lists_words',
#                     'timestamp': datetime.now().isoformat()
#                 })
#         except Exception as e:
#             origin = _exception_origin(e)
#             error_info = {
#                 'iteration': i + 1,
#                 'error_type': type(e).__name__,
#                 'error_message': str(e),
#                 'tested_function': 'lists_words',
#                 **origin,
#                 'traceback': traceback.format_exc(),
#                 'timestamp': datetime.now().isoformat()
#             }
#             errors.append(error_info)
#             print(f"Ошибка на итерации {i + 1}: {type(e).__name__}: {str(e)}")
    
#     # Записываем ошибки в файл errors.json
#     if errors:
#         with open('errors.json', 'w', encoding='utf-8') as f:
#             json.dump(errors, f, ensure_ascii=False, indent=2)
#         print(f"\nНайдено {len(errors)} ошибок. Записано в errors.json")
#     else:
#         print(f"\nВсе {iterations} прогонов прошли успешно. Ошибок не обнаружено.")
    
#     return len(errors)

# # Запуск тестирования
# if __name__ == "__main__":
#     print(f"Начинаю тестирование функции lists_words")
#     error_count = test_lists_words(1000)
#     print(f"Тестирование завершено. Всего ошибок: {error_count}")

