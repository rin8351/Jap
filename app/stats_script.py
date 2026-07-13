# -*- coding: utf-8 -*-
"""
SRS statistics for the Japanese vocabulary test.
Stored in SQLite (Jp.db). Functions with the _db suffix work with the database.
"""
from datetime import datetime, date
import random

# Intervals (days): when to show a word again after last_right
# Initial interval bases (also used when promoting/demoting difficulty)
EASY_DAYS_INITIAL = 4
NORMAL_DAYS_INITIAL = 2
# Geometric progression: next interval = current * multiplier (capped at MAX_INTERVAL_DAYS)
# normal: 2 -> 4 -> 8 -> 16 -> ... -> 190 (cap)
# easy:   4 -> 10 -> 25 -> ~62 -> ~155 -> 190 (cap)
NORMAL_INTERVAL_MULTIPLIER = 2.0   # double after each correct answer
EASY_INTERVAL_MULTIPLIER = 2.5     # easy words grow faster
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
    Unique key of an item: (num_key, item_key).
    item_key = "question|answer" (e.g. "一|one") if answer_column is given,
    otherwise just the question value (for backward compatibility).
    """
    num = item.get("Num")
    q = str(item.get(question, "")).strip()
    if answer_column is not None:
        a = str(item.get(answer_column, "")).strip()
        return str(num), f"{q}|{a}"
    return str(num), f"{q}"


def _ensure_num(stats, num_key):
    """Top level of stats is keyed by Num. Under each Num, slices by question|answer pairs."""
    if num_key not in stats:
        stats[num_key] = {}
    return stats[num_key]


def _difficulty_rank(d):
    """Weakest first: hard=0, normal=1, easy=2."""
    return {"hard": 0, "normal": 1, "easy": 2}.get(d, 1)


def sort_items_for_choice_test(items, stats=None, question=None, answer_column=None):
    """
    SRS presentation order for a test session (used by standard and 4-choice modes).
    Sorting: words not yet in stats first (in_stats=0), then the rest.
    Among the rest: by level (hard -> normal -> easy), within a level by descending wrong,
    and random order when wrong is equal.
    """
    keyed = []
    for item in items:
        num_key, item_key = get_item_key(item, question, answer_column)
        stat = (stats.get(num_key) or {}).get(item_key)
        in_stats = 1 if stat else 0  # 0 = not in stats (shown first), 1 = present
        if not stat:
            stat = {}
        difficulty = stat.get("difficulty", "normal")
        wrong = stat.get("wrong", 0)
        keyed.append((in_stats, _difficulty_rank(difficulty), -wrong, random.random(), item))
    keyed.sort(key=lambda x: (x[0], x[1], x[2], x[3]))
    return [x[4] for x in keyed]


def get_or_create_stat(stats, item, question=None, answer_column=None):
    """Returns the stats dict for an item."""
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
    Checks whether an item should be included in the test based on a single stat record.
    Returns (include: bool, extra_copies: int).
    extra_copies: 0 = once, 1 = add one more time (for hard with wrong >= 3).
    """
    if not stat:
        # New item (not yet recorded) — show it
        return True, 0
    difficulty = stat.get("difficulty", "normal")
    wrong = stat.get("wrong", 0)
    if difficulty == "hard":
        return True, (1 if wrong >= 3 else 0)  # 1 extra = 2 copies total
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
    Returns the list of items for an SRS test.
    answer_column — a single answer column (for backward compatibility).
    answer_columns — a list of answer columns; if given, used instead of answer_column.
    Logic with multiple columns: an item is included if at least one of the
    selected stat tables meets a condition: new item, hard, wrong > 0,
    or the interval date has arrived. Only the selected columns (tables) are checked.
    Conditions per record:
    - new (no stats): always include;
    - hard: always; with wrong >= 3 — twice;
    - wrong > 0: always include;
    - normal/easy: include only if interval_days have passed since last_right.
    - Duplicates by Num are dropped (the first occurrence is kept), except hard doubling.
    """
    today = date.today()
    columns = answer_columns if answer_columns is not None else ([answer_column] if answer_column is not None else [])
    if not columns:
        return []

    # Remove duplicates by Num — keep the first occurrence of each card
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
    Repeat mode: include only items that have stats with difficulty in {normal, easy}
    and that pass the SRS check (wrong > 0 or the interval date has arrived).

    Important:
    - New items (without a stat record) are excluded.
    - hard items are fully excluded.
    - With multiple answer columns: an item is included if at least one selected column
      has a stat record (normal/easy) that qualifies per _stat_qualifies_for_test.
    - Duplicates by Num are dropped (the first occurrence is kept).
    """
    today = date.today()
    if stats is None:
        stats = {}
    columns = answer_columns if answer_columns is not None else ([answer_column] if answer_column is not None else [])
    if not columns:
        return []

    # Remove duplicates by Num — keep the first occurrence of each card
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
                continue  # exclude new items
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
    Records a correct answer: resets wrong, updates last_right, right_all, right and interval_days.
    Automatic difficulty changes (manual Easy/Hard are handled by set_difficulty_only):
    - hard -> normal: after 3 correct answers in a row;
    - normal -> easy: after 4 correct answers in a row.
    On promotion, the streak resets and interval_days is set to the new level's initial value.
    Otherwise the interval grows by the level's multiplier (capped at MAX_INTERVAL_DAYS).
    """
    stat = get_or_create_stat(stats, item, question, answer_column)

    stat["last_right"] = date.today().strftime("%d.%m.%Y")
    stat["wrong"] = 0  # correct answer — reset the error counter, the word goes back on its interval
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
    Manual difficulty change via the Easy/Hard buttons.
    Other counters (right, wrong, last_right, etc.) are untouched.
    difficulty: "easy", "hard" or "normal".
    Setting "easy" also resets interval_days to EASY_DAYS_INITIAL.
    """
    stat = get_or_create_stat(stats, item, question, answer_column)
    stat["difficulty"] = difficulty
    if difficulty == "easy":
        stat["interval_days"] = EASY_DAYS_INITIAL


def record_wrong(stats, item, question=None, answer_column=None):
    """
    +1 wrong, right = 0.
    After 3 errors in a row: normal -> hard (interval_days = 1), easy -> normal
    (interval_days = NORMAL_DAYS_INITIAL). hard stays hard (and with wrong >= 3 is shown twice).
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
    """If difficulty is already 'hard', do not show the 'Easy' button."""
    stat = get_or_create_stat(stats, item, question, answer_column)
    return stat.get("difficulty") != "hard"


# ---------- Working with SQLite ----------

# Dictionary table -> (stats table prefix, question/answer columns used in the test)
STATS_SOURCES = {
    'Kanji': ('kanji', ('Trans', 'Kanji', 'Kun', 'On')),
    'Words': ('words', ('Trans', 'Kanji', 'Read')),
    'Kana': ('kana', ('Trans', 'Kun')),
    'Frazes': ('frazes', ('Trans', 'Kanji', 'Read')),
    'Name': ('name', ('Kanji', 'Read')),
}

SYNC_COLUMNS_BY_SOURCE = {table: cols for table, (_, cols) in STATS_SOURCES.items()}
STATS_PREFIXES = tuple({prefix for prefix, _ in STATS_SOURCES.values()})


def stats_table_name(prefix, question_col, answer_col):
    """Stats table name: {prefix}_{question}_{answer} in lowercase."""
    return f'{prefix}_{question_col.lower()}_{answer_col.lower()}'


def iter_stats_table_names(prefix, columns):
    """All direction pairs (question, answer) for the test columns."""
    for question_col in columns:
        for answer_col in columns:
            if question_col != answer_col:
                yield stats_table_name(prefix, question_col, answer_col)


def stats_column_role(table_name, column_name):
    """
    In a table prefix_Q_A, column Q is synced into value, A into answer.
    """
    parts = str(table_name).lower().split('_', 2)
    if len(parts) >= 2 and parts[1] == str(column_name).lower():
        return 'value'
    return 'answer'


def _cell_has_value(val):
    if val is None:
        return False
    if val == 0 or val == '0':
        return False
    if isinstance(val, str) and val.strip() == '':
        return False
    try:
        import math
        if isinstance(val, float) and math.isnan(val):
            return False
    except (TypeError, ValueError):
        pass
    return True


def populate_stats_tables_for_source(conn, source_table):
    """
    Creates stats tables for source_table and fills them with rows from the dictionary.
    Existing records (num, value, answer) are not overwritten — SRS progress is preserved.
    """
    spec = STATS_SOURCES.get(source_table)
    if not spec:
        return 0
    prefix, columns = spec
    cur = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (source_table,),
    )
    if not cur.fetchone():
        return 0
    cur = conn.execute(f'SELECT * FROM "{source_table}"')
    col_names = [d[0] for d in cur.description]
    if 'Num' not in col_names:
        return 0
    num_idx = col_names.index('Num')
    inserted = 0
    insert_sql = (
        'INSERT INTO "{table}" (num, value, answer, difficulty, wrong, "right", '
        'last_right, interval_days, right_all, wrong_all) '
        'VALUES (?, ?, ?, ?, 0, 0, NULL, 0, 0, 0)'
    )
    for row in cur.fetchall():
        num_key = str(row[num_idx]) if row[num_idx] is not None else ''
        for question_col, answer_col in (
            (q, a) for q in columns for a in columns if q != a
        ):
            if question_col not in col_names or answer_col not in col_names:
                continue
            q_val, a_val = row[col_names.index(question_col)], row[col_names.index(answer_col)]
            if not _cell_has_value(q_val) or not _cell_has_value(a_val):
                continue
            value_part = str(q_val).strip()
            answer_part = str(a_val).strip()
            table_name = stats_table_name(prefix, question_col, answer_col)
            ensure_stats_table_exists(conn, table_name)
            exists = conn.execute(
                f'SELECT 1 FROM "{table_name}" WHERE num = ? AND value = ? AND answer = ?',
                (num_key, value_part, answer_part),
            ).fetchone()
            if exists:
                continue
            conn.execute(
                insert_sql.format(table=table_name),
                (num_key, value_part, answer_part, 'normal'),
            )
            inserted += 1
    conn.commit()
    return inserted


def ensure_all_stats_tables(conn, source_tables=None):
    """Creates and tops up stats tables for the given dictionary tables (default: all in STATS_SOURCES)."""
    tables = source_tables if source_tables is not None else list(STATS_SOURCES.keys())
    total = 0
    for source_table in tables:
        total += populate_stats_tables_for_source(conn, source_table)
    return total


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
    """Converts a DB row (tuple/list) into a stats dict."""
    # Order: num, value, answer, difficulty, wrong, right, last_right, interval_days, right_all, wrong_all
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
    """Creates the stats table if it does not exist yet."""
    conn.execute(STATS_TABLE_SCHEMA.format(table=table_name))
    # DDL — write operation: commit immediately to avoid leaving an open transaction (database is locked)
    conn.commit()



def load_stats_from_db(conn, stats_tables):
    """
    Loads stats from the DB for a list of (col, table_name).
    Returns a merged dict like _merge_stats: num_key -> { item_key -> stat }.
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
    # End the read transaction so it doesn't block later writes (database is locked)
    conn.rollback()
    return merged


def get_or_create_stat_db(conn, table_name, item, question, answer_column):
    """
    Returns the stats dict for an item from the DB; if missing, creates a record and returns defaults.
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
        # End the open transaction to avoid blocking writes to the table (database is locked)
        conn.rollback()
        return _row_to_stat(row)

    # New record
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
    """Writes the stat dict to the DB for the given item."""
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
    Records a correct answer in the DB (same rules as record_correct).
    Returns the updated stats dict (to refresh self.stats).
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
    +1 wrong in the DB (same rules as record_wrong). Returns the updated stats dict.
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
    """Manual difficulty change in the DB (same rules as set_difficulty_only). Returns the updated stats dict."""
    stat = get_or_create_stat_db(conn, table_name, item, question, answer_column)
    stat["difficulty"] = difficulty
    if difficulty == "easy":
        stat["interval_days"] = EASY_DAYS_INITIAL
    _update_stat_in_db(conn, table_name, item, question, answer_column, stat)
    return stat


def can_press_easy_db(conn, table_name, item, question=None, answer_column=None):
    """DB check: whether the 'Easy' button can be shown (not hard)."""
    stat = get_or_create_stat_db(conn, table_name, item, question, answer_column)
    return stat.get("difficulty") != "hard"