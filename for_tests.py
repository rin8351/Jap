from Grammar.filling import *
from Grammar.dop_functions import *
from Grammar.fill_dates import *
from Grammar.fill_numbers import *

print("thousand():", thousand())
print("man():", man())
print("ten_man():", ten_man())
print("hundred_million():", hundred_million())


#Скрипт для тестирования функции lists_words с записью ошибок
# import json
# import traceback
# from datetime import datetime

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
#                     'timestamp': datetime.now().isoformat()
#                 })
#         except Exception as e:
#             error_info = {
#                 'iteration': i + 1,
#                 'error_type': type(e).__name__,
#                 'error_message': str(e),
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
#     error_count = test_lists_words(100)
#     print(f"Тестирование завершено. Всего ошибок: {error_count}")
