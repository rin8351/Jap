import json
import os
import random

# Файл статистики: сколько раз каждая функция была выбрана в вопросе
GRAMMAR_STATS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'grammar_function_stats.json')


def load_grammar_function_stats():
    """Загружает счётчики выбора функций из файла."""
    if not os.path.isfile(GRAMMAR_STATS_FILE):
        return {}
    try:
        with open(GRAMMAR_STATS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_grammar_function_stats(stats):
    """Сохраняет счётчики в файл."""
    try:
        with open(GRAMMAR_STATS_FILE, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


def get_function_key(question, test_style):
    """Возвращает ключ функции для вопроса: item[3] если есть, иначе test_style."""
    if callable(question):
        return getattr(question, '__name__', test_style)
    try:
        if len(question) >= 4:
            return question[3]
    except TypeError:
        pass
    return test_style


def choose_question_by_least_used(spisok_all, test_style):
    """
    Выбирает один вопрос из spisok_all так, чтобы приоритет был у функций
    с наименьшим счётчиком; при равных счётчиках — случайный среди них.
    """
    stats = load_grammar_function_stats()
    # Считаем минимальный счётчик среди функций, представленных в spisok_all
    counts = []
    for q in spisok_all:
        key = get_function_key(q, test_style)
        cnt = stats.get(key, 0)
        counts.append((cnt, q))
    if not counts:
        return None
    min_count = min(c[0] for c in counts)
    # Выбираем только вопросы с минимальным счётчиком
    candidates = [q for c, q in counts if c == min_count]
    return random.choice(candidates)


def increment_function_stats(function_key):
    """Увеличивает счётчик выбора функции на 1 и сохраняет файл."""
    stats = load_grammar_function_stats()
    stats[function_key] = stats.get(function_key, 0) + 1
    save_grammar_function_stats(stats)