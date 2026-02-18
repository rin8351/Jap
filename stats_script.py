# -*- coding: utf-8 -*-
"""
SRS-статистика для теста японских слов.
"""
import json
from datetime import datetime, date
from pathlib import Path
import random

# Интервалы (дней): когда показывать слово после last_right
EASY_DAYS_INITIAL = 2
EASY_DAYS_ADD = 2
NORMAL_DAYS_INITIAL = 1
NORMAL_DAYS_ADD = 1


def _parse_date(s):
    if not s:
        return None
    try:
        return datetime.strptime(s, "%d.%m.%Y").date()
    except ValueError:
        return None



def get_item_key(item, question, answer_column=None):
    """
    Уникальный ключ элемента: (num_key, item_key).
    item_key = "вопрос|ответ" (например "一|один"), если задан answer_column,
    иначе только значение вопроса (для обратной совместимости).
    """
    num = item.get("Num")
    q = item.get(question, "")
    if answer_column is not None:
        a = item.get(answer_column, "")
        return str(num), f"{q}|{a}"
    return str(num), f"{q}"



def save_stats(stats, name_of_file):
    with open(name_of_file, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)


def _ensure_num(stats, num_key):
    """Верхний уровень stats — по номерам (Num). Под каждым номером — разрезы по парам вопрос|ответ."""
    if num_key not in stats:
        stats[num_key] = {}
    return stats[num_key]


def _difficulty_rank(d):
    """Слабые первые: hard=0, normal=1, easy=2."""
    return {"hard": 0, "normal": 1, "easy": 2}.get(d, 1)


def sort_items_for_choice_test(items, stats=None, question=None, answer_column=None):
    """
    Для режима с 4 вариантами: статистика не меняется, порядок — слабые первые.
    Сортировка: сначала слова, которых ещё нет в stats (in_stats=0), затем остальные.
    Среди остальных: по уровню (hard → normal → easy), внутри уровня по убыванию wrong,
    при равном wrong — случайный порядок.
    """
    keyed = []
    for item in items:
        num_key, item_key = get_item_key(item, question, answer_column)
        stat = (stats.get(num_key) or {}).get(item_key)
        in_stats = 1 if stat else 0  # 0 — нет в статистике (первые), 1 — есть
        if not stat:
            stat = {}
        difficulty = stat.get("difficulty", "normal")
        wrong = stat.get("wrong", 0)
        keyed.append((in_stats, _difficulty_rank(difficulty), -wrong, random.random(), item))
    keyed.sort(key=lambda x: (x[0], x[1], x[2], x[3]))
    return [x[4] for x in keyed]


def get_or_create_stat(stats, item, question=None, answer_column=None):
    """Возвращает словарь статистики для элемента"""
    num_key, item_key = get_item_key(item, question, answer_column)
    by_num = _ensure_num(stats, num_key)
    if item_key not in by_num:
        by_num[item_key] = {
            "difficulty": "normal",
            "wrong": 0,
            "right": 0,
            "last_right": None,
            "interval_days": NORMAL_DAYS_INITIAL,
            "consecutive_wrong": 0,
        }
    return by_num[item_key]


def filter_items_for_test(items, stats=None, question=None, answer_column=None):
    """
    Возвращает список элементов для теста по SRS:
    - easy: показывать только если прошло interval_days после last_right.
    - normal: то же, свой интервал.
    - hard: всегда; если wrong == 2 — 2 раза, если wrong >= 3 — 3 раза.
    - Любое слово с wrong > 0 показывается в каждом тесте (нужно выучить, пока не ответишь правильно).
    - Дубликаты по Num отбрасываются (остаётся первое вхождение).
    """
    today = date.today()
    # Убираем дубликаты по Num — оставляем первое вхождение каждой карточки
    seen_num = set()
    items_unique = []
    for item in items:
        num = item.get("Num")
        if num not in seen_num:
            seen_num.add(num)
            items_unique.append(item)
    items = items_unique
    result = []

    for item in items:
        num_key, item_key = get_item_key(item, question, answer_column)
        by_num = stats.get(num_key, {})
        stat = by_num.get(item_key)
        if not stat:
            # Нет статистики — считаем нормальным, показываем
            result.append(item)
            continue

        difficulty = stat.get("difficulty", "normal")
        wrong = stat.get("wrong", 0)


        if difficulty == "hard":
            if wrong >= 3:
                result.extend([item, item])
            else:
                result.append(item)
            continue

        # Слова с хотя бы одной ошибкой всегда в тесте — пока не ответить правильно
        if wrong > 0:
            result.append(item)
            continue

        if difficulty == "easy":
            interval = stat.get("interval_days", EASY_DAYS_INITIAL)
        else:
            interval = stat.get("interval_days", NORMAL_DAYS_INITIAL)

        last_right = _parse_date(stat.get("last_right"))
        if last_right is None:
            result.append(item)
            continue
        days = (today - last_right).days
        if days >= interval:
            result.append(item)

    return result


def record_correct(stats, item, difficulty_button=None, question=None, name_of_file=None, answer_column=None):
    """
    difficulty_button: None, "easy", "hard". question — имя колонки (напр. "Kanji", "Trans"), по ней из item берётся ключ для статистики.
    answer_column — колонка ответа; ключ в статистике будет "вопрос|ответ".
    - Если "easy": ставим difficulty = "easy" (если не hard).
    - Если "hard": ставим difficulty = "hard".
    - Увеличиваем right, сбрасываем consecutive_wrong, обновляем last_right и interval_days.
    - normal → easy: после 4 правильных подряд (уже учтено через right); при нажатии "easy" или при right==4 сбрасываем right и ставим easy.
    - hard → normal: после 2 правильных (сбрасываем right и ставим normal).
    """
    if not isinstance(difficulty_button, str):
        difficulty_button = None
    stat = get_or_create_stat(stats, item, question, answer_column)

    stat["consecutive_wrong"] = 0
    stat["last_right"] = date.today().strftime("%d.%m.%Y")
    stat["wrong"] = 0  # правильный ответ — сбрасываем счётчик ошибок, слово снова по интервалу
    stat["right_all"] = stat.get("right_all", 0) + 1
    stat["wrong_all"] = stat.get("wrong_all", 0)

    if difficulty_button == "hard":
        stat["difficulty"] = "hard"
        stat["right"] = 0
        stat["interval_days"] = NORMAL_DAYS_INITIAL
        save_stats(stats, name_of_file)
        return

    if difficulty_button == "easy":
        if stat.get("difficulty") != "hard":
            stat["difficulty"] = "easy"
            stat["right"] = 0
            stat["interval_days"] = EASY_DAYS_INITIAL
        save_stats(stats, name_of_file)
        return

    # Обычное "Правильно" без кнопки сложности
    difficulty = stat.get("difficulty", "normal")
    right = stat.get("right", 0) + 1

    if difficulty == "hard":
        if right == 3:
            stat["difficulty"] = "normal"
            stat["right"] = 0
            stat["interval_days"] = NORMAL_DAYS_INITIAL
        else:
            stat["right"] = right
        save_stats(stats, name_of_file)
        return

    if difficulty == "normal":
        if right == 4:
            stat["difficulty"] = "easy"
            stat["right"] = 0
            stat["interval_days"] = EASY_DAYS_INITIAL
        else:
            stat["right"] = right
            if stat["interval_days"] < 30:
                stat["interval_days"] = stat.get("interval_days", NORMAL_DAYS_INITIAL) + NORMAL_DAYS_ADD
            else:
                stat["interval_days"] = 30
        save_stats(stats, name_of_file)
        return
        
    if difficulty == "easy":
        stat["right"] = right
        if stat["interval_days"] < 30:
            stat["interval_days"] = stat.get("interval_days", EASY_DAYS_INITIAL) + EASY_DAYS_ADD
        else:
            stat["interval_days"] = 30
        save_stats(stats, name_of_file)
        return


def set_difficulty_only(stats, item, difficulty, question=None, name_of_file=None, answer_column=None):
    """
    Меняет только ключ difficulty для элемента. Остальная статистика (right, wrong, last_right и т.д.) не трогается.
    difficulty: "easy", "hard" или "normal".
    """
    stat = get_or_create_stat(stats, item, question, answer_column)
    stat["difficulty"] = difficulty
    save_stats(stats, name_of_file)


def record_wrong(stats, item, question=None, name_of_file=None, answer_column=None):
    """
    +1 wrong, +1 consecutive_wrong, right = 0.
    Если consecutive_wrong >= 2: normal → hard, easy → normal.
    """
    stat = get_or_create_stat(stats, item, question, answer_column)
    stat["wrong"] = stat.get("wrong", 0) + 1
    stat["consecutive_wrong"] = stat.get("consecutive_wrong", 0) + 1
    stat["right"] = 0
    stat["wrong_all"] = stat.get("wrong_all", 0) + 1
    stat["right_all"] = stat.get("right_all", 0)

    if stat["consecutive_wrong"] >= 2:
        d = stat.get("difficulty", "normal")
        if d == "normal":
            stat["difficulty"] = "hard"
        elif d == "easy":
            stat["difficulty"] = "normal"
        stat["interval_days"] = NORMAL_DAYS_INITIAL

    save_stats(stats, name_of_file)


def can_press_easy(stats, item, question=None, answer_column=None):
    """Если сложность уже 'hard', кнопку 'Легко' не показывать."""
    stat = get_or_create_stat(stats, item, question, answer_column)
    return stat.get("difficulty") != "hard"
