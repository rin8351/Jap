from Grammar.filling import *
from Grammar.dop_functions import *
from Grammar.fill_dates import *
from Grammar.fill_numbers import *

#print( concessive_subordinate_noni())

#glag_im_doing

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


stat = [
   [{'index': 15, 'Lesson': 1, 'Num': 27, 'Kanji': '文', 'On': '0', 'Kun': 'もん', 'Trans': 'предложение, письмо', 'Sush': 'Сущ', 'Mnem': '0'}, {'index': 17, 'Lesson': 1, 'Num': 25, 'Kanji': '日', 'On': 'ニチ、ジツ', 'Kun': 'ひ、か', 'Trans': 'день, солнце', 'Sush': 'Сущ', 'Mnem': 'буквально квадратное солнце с прищуренным глазом'}, {'index': 10, 'Lesson': 1, 'Num': 34, 'Kanji': '何', 'On': 'カ', 'Kun': 'なに、なん', 'Trans': 'что', 'Sush': 'Сущ', 'Mnem': 'два человека о чем то разговаривают'}, {'index': 12, 'Lesson': 1, 'Num': 35, 'Kanji': '学', 'On': 'ガク', 'Kun': '0', 'Trans': 'учёба', 'Sush': 'Сущ', 'Mnem': 'ребенок просветляется'}, {'index': 8, 'Lesson': 1, 'Num': 21, 'Kanji': '一', 'On': 'イチ、イツ', 'Kun': 'ひとつ', 'Trans': 'один', 'Sush': 'Сущ', 'Mnem': 'одна черта'}, {'index': 20, 'Lesson': 1, 'Num': 33, 'Kanji': '生', 'On': '0', 'Kun': 'なま', 'Trans': 'сырой, неспелый', 'Sush': 'Сущ', 'Mnem': '0'}, {'index': 18, 'Lesson': 1, 'Num': 30, 'Kanji': '生', 'On': 'セイ、ショウ', 'Kun': '0', 'Trans': 'жизнь, живой', 'Sush': 'Сущ', 'Mnem': 'из земли рождается росток'}, {'index': 21, 'Lesson': 1, 'Num': 37, 'Kanji': '語', 'On': 'ゴ', 'Kun': '0', 'Trans': 'слово, язык', 'Sush': 'Сущ', 'Mnem': 'говорят 5 ртов'}, {'index': 11, 'Lesson': 1, 'Num': 29, 'Kanji': '先', 'On': 'セン', 'Kun': 'さき', 'Trans': 'раньше, впереди', 'Sush': 'Сущ', 'Mnem': 'впеерди всего- жизнь- из земли вырастает что то с корнями'}, {'index': 14, 'Lesson': 1, 'Num': 26, 'Kanji': '文', 'On': 'ブン', 'Kun': '0', 'Trans': 'литература, текст, культура', 'Sush': 'Сущ', 'Mnem': 'как будто человека скрутило от культуры'}, {'index': 9, 'Lesson': 1, 'Num': 22, 'Kanji': '人', 'On': 'ニン、ジン', 'Kun': 'ひと', 'Trans': 'человек, люди', 'Sush': 'Сущ', 'Mnem': 'две ножки человека'}, {'index': 16, 'Lesson': 1, 'Num': 24, 'Kanji': '方', 'On': '0', 'Kun': 'かた', 'Trans': 'человек, лицо', 'Sush': 'Сущ', 'Mnem': 'в правую сторону бегу'}]
]
