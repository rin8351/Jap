# -*- coding: utf-8 -*-
"""
SRS-статистика для теста японских слов.
Хранение в SQLite (Jp.db). Функции с суффиксом _db работают с БД.
"""
from datetime import datetime, date
import random

# Интервалы (дней): когда показывать слово после last_right
# Начальные интервалы после первого правильного ответа
EASY_DAYS_INITIAL = 4
NORMAL_DAYS_INITIAL = 2
# Геометрическая прогрессия: следующий интервал = текущий * множитель
# normal: 2 → 4 → 8 → 16 → 30 (cap)
# easy: 4 → 10 → 25 → 30 (cap)
NORMAL_INTERVAL_MULTIPLIER = 2.0   # удвоение после каждого правильного
EASY_INTERVAL_MULTIPLIER = 2.5     # для лёгких рост быстрее
MAX_INTERVAL_DAYS = 190


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
    q = str(item.get(question, "")).strip()
    if answer_column is not None:
        a = str(item.get(answer_column, "")).strip()
        return str(num), f"{q}|{a}"
    return str(num), f"{q}"


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
            "interval_days": 0,
        }
    return by_num[item_key]


def _stat_qualifies_for_test(stat, today):
    """
    Проверяет, нужно ли включать элемент в тест по одной записи статистики.
    Возвращает (include: bool, extra_copies: int).
    extra_copies: 0 = один раз, 1 = добавить ещё один раз (для hard с wrong >= 3).
    """
    if not stat:
        # Новый элемент (его ещё нет в файле) — показываем
        return True, 0
    difficulty = stat.get("difficulty", "normal")
    wrong = stat.get("wrong", 0)
    if difficulty == "hard":
        return True, (1 if wrong >= 3 else 0)  # 1 extra = всего 2 копии
    if wrong > 0:
        return True, 0
    if difficulty == "easy":
        interval = stat.get("interval_days", EASY_DAYS_INITIAL)
    else:
        interval = stat.get("interval_days", NORMAL_DAYS_INITIAL)
    last_right = _parse_date(stat.get("last_right"))
    if last_right is None:
        return True, 0
    days = (today - last_right).days
    return (days >= interval, 0)


def filter_items_for_test(items, stats=None, question=None, answer_column=None, answer_columns=None):
    """
    Возвращает список элементов для теста по SRS.
    answer_column — одна колонка ответа (для обратной совместимости).
    answer_columns — список колонок ответа; если задан, используется вместо answer_column.
    Логика при нескольких колонках: элемент попадает в тест, если хотя бы в одном
    из выбранных файлов статистики выполняются условия: новый элемент, hard, wrong > 0
    или наступила дата по интервалу. Проверяются только выбранные колонки (файлы).
    Условия по одной записи:
    - easy: показывать только если прошло interval_days после last_right.
    - normal: то же, свой интервал.
    - hard: всегда; при wrong >= 3 — два раза.
    - wrong > 0: всегда в тесте.
    - Дубликаты по Num отбрасываются (остаётся первое вхождение).
    """
    today = date.today()
    columns = answer_columns if answer_columns is not None else ([answer_column] if answer_column is not None else [])
    if not columns:
        return []

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
        include = False
        extra = 0
        for col in columns:
            val = item.get(col, "")
            if not str(val).strip() or str(val) == "0":
                continue
            num_key, item_key = get_item_key(item, question, col)
            by_num = stats.get(num_key, {})
            stat = by_num.get(item_key)
            qual, ext = _stat_qualifies_for_test(stat, today)
            if qual:
                include = True
                if ext > extra:
                    extra = ext
        if include:
            result.append(item)
            for _ in range(extra):
                result.append(item)

    return result


def filter_items_for_repeat(items, stats=None, question=None, answer_column=None, answer_columns=None):
    """
    Режим повтора: включаем только элементы со статистикой, у которых difficulty ∈ {normal, easy},
    и которые проходят SRS-проверку (wrong > 0 или наступила дата по интервалу).

    Важно:
    - Новые элементы (без записи в stats) исключаются.
    - hard исключаются полностью.
    - При нескольких колонках ответа: элемент включается, если хотя бы по одной выбранной колонке
      есть запись в stats (normal/easy) и она qualifies по _stat_qualifies_for_test.
    - Дубликаты по Num отбрасываются (остаётся первое вхождение).
    """
    today = date.today()
    if stats is None:
        stats = {}
    columns = answer_columns if answer_columns is not None else ([answer_column] if answer_column is not None else [])
    if not columns:
        return []

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
        include = False
        for col in columns:
            val = item.get(col, "")
            if not str(val).strip() or str(val) == "0":
                continue
            num_key, item_key = get_item_key(item, question, col)
            by_num = stats.get(num_key, {})
            stat = by_num.get(item_key)
            if not stat:
                continue  # новые исключаем
            difficulty = stat.get("difficulty", "normal")
            if difficulty == "hard":
                continue
            qual, _ext = _stat_qualifies_for_test(stat, today)
            if qual:
                include = True
                break
        if include:
            result.append(item)

    return result


def record_correct(stats, item, question=None, answer_column=None):
    """
    Учитывает правильный ответ: сбрасывает wrong, обновляет last_right, right_all, right и interval_days.
    Сложность (easy/hard) меняется только через кнопки «Легко»/«Сложно» (set_difficulty_only в UI).
    - hard → normal: после 2 правильных подряд.
    - normal → easy: после 4 правильных подряд.
    """
    stat = get_or_create_stat(stats, item, question, answer_column)

    stat["last_right"] = date.today().strftime("%d.%m.%Y")
    stat["wrong"] = 0  # правильный ответ — сбрасываем счётчик ошибок, слово снова по интервалу
    stat["right_all"] = stat.get("right_all", 0) + 1
    stat["wrong_all"] = stat.get("wrong_all", 0)

    difficulty = stat.get("difficulty", "normal")
    right = stat.get("right", 0) + 1

    if difficulty == "hard":
        if right == 3:
            stat["difficulty"] = "normal"
            stat["right"] = 0
            stat["interval_days"] = NORMAL_DAYS_INITIAL
        else:
            stat["right"] = right
        return

    if difficulty == "normal":
        if right == 4:
            stat["difficulty"] = "easy"
            stat["right"] = 0
            stat["interval_days"] = EASY_DAYS_INITIAL
        else:
            stat["right"] = right
            current = stat.get("interval_days") or NORMAL_DAYS_INITIAL
            if current == 0:
                current = NORMAL_DAYS_INITIAL
            stat["interval_days"] = min(
                round(current * NORMAL_INTERVAL_MULTIPLIER),
                MAX_INTERVAL_DAYS
            )
        return

    if difficulty == "easy":
        stat["right"] = right
        current = stat.get("interval_days") or EASY_DAYS_INITIAL
        if current == 0:
            current = EASY_DAYS_INITIAL
        stat["interval_days"] = min(
            round(current * EASY_INTERVAL_MULTIPLIER),
            MAX_INTERVAL_DAYS
        )
        return


def set_difficulty_only(stats, item, difficulty, question=None, answer_column=None):
    """
    Меняет только ключ difficulty для элемента. Остальная статистика (right, wrong, last_right и т.д.) не трогается.
    difficulty: "easy", "hard" или "normal".
    """
    stat = get_or_create_stat(stats, item, question, answer_column)
    stat["difficulty"] = difficulty
    if difficulty == "easy":
        stat["interval_days"] = EASY_DAYS_INITIAL


def record_wrong(stats, item, question=None, answer_column=None):
    """
    +1 wrong, right = 0.
    Если количество ошибок == 3: normal → hard, easy → normal.
    """
    stat = get_or_create_stat(stats, item, question, answer_column)
    stat["wrong"] = stat.get("wrong", 0) + 1
    stat["right"] = 0
    stat["wrong_all"] = stat.get("wrong_all", 0) + 1
    stat["right_all"] = stat.get("right_all", 0)

    if stat["wrong"] == 3:
        d = stat.get("difficulty", "normal")
        if d == "normal":
            stat["difficulty"] = "hard"
            stat["interval_days"] = 1
        elif d == "easy":
            stat["difficulty"] = "normal"
            stat["interval_days"] = NORMAL_DAYS_INITIAL
        

def can_press_easy(stats, item, question=None, answer_column=None):
    """Если сложность уже 'hard', кнопку 'Легко' не показывать."""
    stat = get_or_create_stat(stats, item, question, answer_column)
    return stat.get("difficulty") != "hard"


# ---------- Работа с SQLite (та же схема, что в migrate_stats_to_db.py) ----------

STATS_TABLE_SCHEMA = '''
    CREATE TABLE IF NOT EXISTS "{table}" (
        num TEXT,
        value TEXT,
        answer TEXT,
        difficulty TEXT,
        wrong INTEGER,
        "right" INTEGER,
        last_right TEXT,
        interval_days INTEGER,
        right_all INTEGER,
        wrong_all INTEGER
    )
'''


def _row_to_stat(row):
    """Преобразует строку БД (tuple/list) в словарь статистики."""
    # Порядок: num, value, answer, difficulty, wrong, right, last_right, interval_days, right_all, wrong_all
    return {
        "difficulty": row[3] or "normal",
        "wrong": int(row[4] or 0),
        "right": int(row[5] or 0),
        "last_right": row[6],
        "interval_days": int(row[7] or 0),
        "right_all": int(row[8] or 0),
        "wrong_all": int(row[9] or 0),
    }


def ensure_stats_table_exists(conn, table_name):
    """Создаёт таблицу статистики, если её ещё нет."""
    conn.execute(STATS_TABLE_SCHEMA.format(table=table_name))


def load_stats_from_db(conn, stats_tables):
    """
    Загружает статистику из БД по списку (col, table_name).
    Возвращает объединённый словарь как _merge_stats: num_key -> { item_key -> stat }.
    """
    merged = {}
    for col, table_name in stats_tables:
        ensure_stats_table_exists(conn, table_name)
        cur = conn.execute(
            f'SELECT num, value, answer, difficulty, wrong, "right", last_right, interval_days, right_all, wrong_all FROM "{table_name}"'
        )
        for row in cur.fetchall():
            num_key = str(row[0]) if row[0] is not None else ""
            value_part = (row[1] or "").strip()
            answer_part = (row[2] or "").strip()
            item_key = f"{value_part}|{answer_part}" if answer_part else value_part
            if num_key not in merged:
                merged[num_key] = {}
            merged[num_key][item_key] = _row_to_stat(row)
    # Завершаем read-транзакцию, чтобы не блокировать последующие записи (database is locked)
    conn.rollback()
    return merged


def get_or_create_stat_db(conn, table_name, item, question, answer_column):
    """
    Возвращает словарь статистики для элемента из БД; при отсутствии создаёт запись и возвращает дефолт.
    """
    ensure_stats_table_exists(conn, table_name)
    num_key, item_key = get_item_key(item, question, answer_column)
    if "|" in item_key:
        value_part, answer_part = item_key.split("|", 1)
    else:
        value_part, answer_part = item_key.strip(), ""
    value_part = value_part.strip()
    answer_part = answer_part.strip()

    cur = conn.execute(
        f'SELECT num, value, answer, difficulty, wrong, "right", last_right, interval_days, right_all, wrong_all FROM "{table_name}" WHERE num = ? AND value = ? AND answer = ?',
        (num_key, value_part, answer_part),
    )
    row = cur.fetchone()
    if row is not None:
        return _row_to_stat(row)

    # Новая запись
    conn.execute(
        f'''INSERT INTO "{table_name}" (num, value, answer, difficulty, wrong, "right", last_right, interval_days, right_all, wrong_all)
            VALUES (?, ?, ?, ?, 0, 0, NULL, 0, 0, 0)''',
        (num_key, value_part, answer_part, "normal"),
    )
    conn.commit()
    return {
        "difficulty": "normal",
        "wrong": 0,
        "right": 0,
        "last_right": None,
        "interval_days": 0,
        "right_all": 0,
        "wrong_all": 0,
    }


def _update_stat_in_db(conn, table_name, item, question, answer_column, stat):
    """Записывает словарь stat в БД для данного элемента."""
    num_key, item_key = get_item_key(item, question, answer_column)
    if "|" in item_key:
        value_part, answer_part = item_key.split("|", 1)
    else:
        value_part, answer_part = item_key.strip(), ""
    value_part = value_part.strip()
    answer_part = answer_part.strip()

    conn.execute(
        f'''UPDATE "{table_name}" SET difficulty = ?, wrong = ?, "right" = ?, last_right = ?, interval_days = ?, right_all = ?, wrong_all = ?
            WHERE num = ? AND value = ? AND answer = ?''',
        (
            stat.get("difficulty", "normal"),
            int(stat.get("wrong", 0)),
            int(stat.get("right", 0)),
            stat.get("last_right"),
            int(stat.get("interval_days", 0)),
            int(stat.get("right_all", 0)),
            int(stat.get("wrong_all", 0)),
            num_key,
            value_part,
            answer_part,
        ),
    )
    conn.commit()


def record_correct_db(conn, table_name, item, question=None, answer_column=None):
    """
    Учитывает правильный ответ в БД. Возвращает обновлённый словарь статистики (для обновления self.stats).
    """
    stat = get_or_create_stat_db(conn, table_name, item, question, answer_column)

    stat["last_right"] = date.today().strftime("%d.%m.%Y")
    stat["wrong"] = 0
    stat["right_all"] = stat.get("right_all", 0) + 1
    stat["wrong_all"] = stat.get("wrong_all", 0)

    difficulty = stat.get("difficulty", "normal")
    right = stat.get("right", 0) + 1

    if difficulty == "hard":
        if right == 3:
            stat["difficulty"] = "normal"
            stat["right"] = 0
            stat["interval_days"] = NORMAL_DAYS_INITIAL
        else:
            stat["right"] = right
    elif difficulty == "normal":
        if right == 4:
            stat["difficulty"] = "easy"
            stat["right"] = 0
            stat["interval_days"] = EASY_DAYS_INITIAL
        else:
            stat["right"] = right
            current = stat.get("interval_days") or NORMAL_DAYS_INITIAL
            if current == 0:
                current = NORMAL_DAYS_INITIAL
            stat["interval_days"] = min(
                round(current * NORMAL_INTERVAL_MULTIPLIER),
                MAX_INTERVAL_DAYS,
            )
    else:  # easy
        stat["right"] = right
        current = stat.get("interval_days") or EASY_DAYS_INITIAL
        if current == 0:
            current = EASY_DAYS_INITIAL
        stat["interval_days"] = min(
            round(current * EASY_INTERVAL_MULTIPLIER),
            MAX_INTERVAL_DAYS,
        )

    _update_stat_in_db(conn, table_name, item, question, answer_column, stat)
    return stat


def record_wrong_db(conn, table_name, item, question=None, answer_column=None):
    """
    +1 wrong в БД. Возвращает обновлённый словарь статистики.
    """
    stat = get_or_create_stat_db(conn, table_name, item, question, answer_column)
    stat["wrong"] = stat.get("wrong", 0) + 1
    stat["right"] = 0
    stat["wrong_all"] = stat.get("wrong_all", 0) + 1
    stat["right_all"] = stat.get("right_all", 0)

    if stat["wrong"] == 3:
        d = stat.get("difficulty", "normal")
        if d == "normal":
            stat["difficulty"] = "hard"
            stat["interval_days"] = 1
        elif d == "easy":
            stat["difficulty"] = "normal"
            stat["interval_days"] = NORMAL_DAYS_INITIAL

    _update_stat_in_db(conn, table_name, item, question, answer_column, stat)
    return stat


def set_difficulty_only_db(conn, table_name, item, difficulty, question=None, answer_column=None):
    """Меняет только difficulty в БД. Возвращает обновлённый словарь статистики."""
    stat = get_or_create_stat_db(conn, table_name, item, question, answer_column)
    stat["difficulty"] = difficulty
    if difficulty == "easy":
        stat["interval_days"] = EASY_DAYS_INITIAL
    _update_stat_in_db(conn, table_name, item, question, answer_column, stat)
    return stat


def can_press_easy_db(conn, table_name, item, question=None, answer_column=None):
    """Проверка по БД: можно ли показывать кнопку «Легко» (не hard)."""
    stat = get_or_create_stat_db(conn, table_name, item, question, answer_column)
    return stat.get("difficulty") != "hard"