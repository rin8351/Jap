# -*- coding: utf-8 -*-
"""Builds reports from the dictionary tables and statistics (Jp.db)."""
from datetime import date
import os
import sqlite3

from stats_script import (
    STATS_SOURCES,
    iter_stats_table_names,
    _parse_date,
    _stat_qualifies_for_test,
    _row_to_stat,
)

DB_NAME = 'Jp.db'
MIN_ATTEMPTS_DEFAULT = 5
SOURCES_WITH_SUSH = frozenset({'Kanji', 'Kana'})
# Part-of-speech codes stored in the DB (Noun, Adjective, Verb, Adverb)
SUSH_ORDER = ['Noun', 'Adjective', 'Verb', 'Adverb']

SOURCE_WORD_COLUMNS = {
    'Kanji': ('Kanji', 'Trans'),
    'Words': ('Kanji', 'Trans'),
    'Kana': ('Kun', 'Trans'),
    'Frazes': ('Kanji', 'Trans'),
    'Name': ('Kanji', 'Read'),
}


def get_db_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), DB_NAME)


def open_db(db_path=None):
    path = db_path or get_db_path()
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def efficiency(right_all, wrong_all):
    total = int(right_all or 0) + int(wrong_all or 0)
    if total <= 0:
        return None
    return int(right_all or 0) / total


def format_pct(value):
    if value is None:
        return '—'
    return f'{value * 100:.1f}%'


def _has_lesson(value):
    """True if the word has a lesson number (not empty and not a dash)."""
    if value is None:
        return False
    return str(value).strip() not in ('', '—')


def _direction_label(table_name, prefix):
    rest = table_name[len(prefix) + 1:]
    parts = rest.split('_', 2)
    if len(parts) >= 2:
        q, a = parts[0], parts[1]
        return f'{q.capitalize()}→{a.capitalize()}'
    return rest


def _word_label(row, source):
    if row is None:
        return ''
    col_a, col_b = SOURCE_WORD_COLUMNS.get(source, ('Kanji', 'Trans'))
    for key in (col_a, col_b, 'Num'):
        val = row.get(key)
        if val is not None and str(val).strip() and str(val) not in ('0', '0.0'):
            return str(val).strip()
    return str(row.get('Num', ''))


def _load_dictionary(conn, source):
    cur = conn.execute(f'SELECT * FROM "{source}"')
    if not cur.description:
        return {}
    names = [d[0] for d in cur.description]
    result = {}
    for row in cur.fetchall():
        item = {names[i]: row[i] for i in range(len(names))}
        num = item.get('Num')
        if num is None:
            continue
        result[str(num)] = item
    return result


def _load_stats_index(conn, source):
    """
    num -> {
        directions: {direction_label: stat_dict},
        ...
    }
    """
    spec = STATS_SOURCES.get(source)
    if not spec:
        return {}
    prefix, _columns = spec
    by_num = {}
    for table_name in iter_stats_table_names(prefix, _columns):
        try:
            cur = conn.execute(
                f'SELECT num, value, answer, difficulty, wrong, "right", last_right, '
                f'interval_days, right_all, wrong_all FROM "{table_name}"'
            )
        except sqlite3.OperationalError:
            continue
        direction = _direction_label(table_name, prefix)
        for row in cur.fetchall():
            num_key = str(row[0]) if row[0] is not None else ''
            stat = _row_to_stat(row)
            entry = by_num.setdefault(num_key, {'directions': {}})
            entry['directions'][direction] = stat
    return by_num


def _aggregate_num(stats_dirs, today):
    directions = stats_dirs or {}
    if not directions:
        return {
            'total_right': 0,
            'total_wrong': 0,
            'attempts': 0,
            'efficiency': None,
            'tested': False,
            'due': True,
            'hard': False,
            'session_wrong': False,
            'days_since': None,
            'directions': {},
        }
    total_right = 0
    total_wrong = 0
    any_tested = False
    due = False
    hard = False
    session_wrong = False
    last_dates = []

    for stat in directions.values():
        ra = int(stat.get('right_all', 0) or 0)
        wa = int(stat.get('wrong_all', 0) or 0)
        total_right += ra
        total_wrong += wa
        if ra + wa > 0:
            any_tested = True
        if stat.get('difficulty') == 'hard':
            hard = True
        if int(stat.get('wrong', 0) or 0) > 0:
            session_wrong = True
        qual, _ = _stat_qualifies_for_test(stat, today)
        if qual:
            due = True
        lr = _parse_date(stat.get('last_right'))
        if lr is not None:
            last_dates.append(lr)

    eff = efficiency(total_right, total_wrong)
    days_since = None
    if last_dates:
        days_since = (today - max(last_dates)).days

    return {
        'total_right': total_right,
        'total_wrong': total_wrong,
        'attempts': total_right + total_wrong,
        'efficiency': eff,
        'tested': any_tested,
        'due': due,
        'hard': hard,
        'session_wrong': session_wrong,
        'days_since': days_since,
        'directions': directions,
    }


def build_num_aggregates(conn, source, today=None, dict_only=False):
    today = today or date.today()
    dictionary = _load_dictionary(conn, source)
    stats_by_num = _load_stats_index(conn, source)
    if dict_only:
        all_nums = set(dictionary)
    else:
        all_nums = set(dictionary) | set(stats_by_num)
    rows = []
    for num in all_nums:
        dict_row = dictionary.get(num)
        stats_entry = stats_by_num.get(num, {})
        agg = _aggregate_num(stats_entry.get('directions', {}), today)
        rows.append({
            'num': num,
            'dict': dict_row,
            'lesson': dict_row.get('Lesson') if dict_row else None,
            'sush': dict_row.get('Sush') if dict_row else None,
            'label': _word_label(dict_row, source),
            **agg,
        })
    return rows


def count_orphaned_stats(conn, source):
    """Stats records whose num no longer exists in the dictionary table."""
    dictionary = _load_dictionary(conn, source)
    stats_by_num = _load_stats_index(conn, source)
    return len(set(stats_by_num) - set(dictionary))


def overview_all_sources(conn, today=None):
    today = today or date.today()
    result = []
    for source in STATS_SOURCES:
        rows = build_num_aggregates(conn, source, today, dict_only=True)
        total = len(rows)
        tested = sum(1 for r in rows if r['tested'])
        due = sum(1 for r in rows if r['due'])
        hard = sum(1 for r in rows if r['hard'])
        never = total - tested
        effs = [r['efficiency'] for r in rows if r['efficiency'] is not None]
        avg_eff = sum(effs) / len(effs) if effs else None
        result.append({
            'source': source,
            'total': total,
            'tested': tested,
            'never': never,
            'due': due,
            'hard': hard,
            'avg_efficiency': avg_eff,
            'pct_tested': (tested / total * 100) if total else 0,
            'orphaned': count_orphaned_stats(conn, source),
        })
    return result


def lesson_breakdown(conn, source, today=None):
    today = today or date.today()
    rows = build_num_aggregates(conn, source, today, dict_only=True)
    groups = {}
    for r in rows:
        lesson = r.get('lesson')
        if not _has_lesson(lesson):
            continue
        key = str(lesson).strip()
        groups.setdefault(key, []).append(r)

    out = []
    for lesson, items in groups.items():
        total = len(items)
        tested = sum(1 for x in items if x['tested'])
        due = sum(1 for x in items if x['due'])
        hard = sum(1 for x in items if x['hard'])
        attempts = sum(x['attempts'] for x in items)
        effs = [x['efficiency'] for x in items if x['efficiency'] is not None]
        days_list = [x['days_since'] for x in items if x['days_since'] is not None]
        max_days = max(days_list) if days_list else None
        out.append({
            'lesson': lesson,
            'total': total,
            'tested_pct': tested / total * 100 if total else 0,
            'due': due,
            'hard': hard,
            'avg_efficiency': sum(effs) / len(effs) if effs else None,
            'days_since': max_days,
            'attempts': attempts,
        })
    out.sort(key=lambda x: (-(x['days_since'] if x['days_since'] is not None else 10**9), x['lesson']))
    return out


def sush_breakdown(conn, source, today=None):
    if source not in SOURCES_WITH_SUSH:
        return []
    today = today or date.today()
    rows = build_num_aggregates(conn, source, today, dict_only=True)
    groups = {}
    for r in rows:
        sush = r.get('sush')
        key = str(sush).strip() if sush is not None and str(sush).strip() else '—'
        groups.setdefault(key, []).append(r)

    out = []
    for sush, items in groups.items():
        total = len(items)
        tested = sum(1 for x in items if x['tested'])
        due = sum(1 for x in items if x['due'])
        hard = sum(1 for x in items if x['hard'])
        attempts = sum(x['attempts'] for x in items)
        effs = [x['efficiency'] for x in items if x['efficiency'] is not None]
        out.append({
            'sush': sush,
            'total': total,
            'tested_pct': tested / total * 100 if total else 0,
            'due': due,
            'hard': hard,
            'avg_efficiency': sum(effs) / len(effs) if effs else None,
            'attempts': attempts,
        })

    def _sush_sort_key(item):
        s = item['sush']
        if s in SUSH_ORDER:
            return (0, SUSH_ORDER.index(s))
        return (1, s)

    out.sort(key=_sush_sort_key)
    return out


def direction_breakdown(conn, source, today=None):
    today = today or date.today()
    stats_by_num = _load_stats_index(conn, source)
    per_dir = {}
    for num, entry in stats_by_num.items():
        for direction, stat in entry.get('directions', {}).items():
            bucket = per_dir.setdefault(direction, [])
            bucket.append(stat)

    out = []
    for direction, stats in per_dir.items():
        total = len(stats)
        due = sum(1 for s in stats if _stat_qualifies_for_test(s, today)[0])
        hard = sum(1 for s in stats if s.get('difficulty') == 'hard')
        effs = [efficiency(s.get('right_all'), s.get('wrong_all')) for s in stats]
        effs = [e for e in effs if e is not None]
        attempts = sum(int(s.get('right_all', 0) or 0) + int(s.get('wrong_all', 0) or 0) for s in stats)
        out.append({
            'direction': direction,
            'total': total,
            'due': due,
            'hard': hard,
            'avg_efficiency': sum(effs) / len(effs) if effs else None,
            'attempts': attempts,
        })
    out.sort(key=lambda x: (x['avg_efficiency'] if x['avg_efficiency'] is not None else 2, x['direction']))
    return out


def word_rankings(conn, source, min_attempts=MIN_ATTEMPTS_DEFAULT, hardest=True, today=None):
    today = today or date.today()
    rows = build_num_aggregates(conn, source, today, dict_only=True)
    filtered = [
        r for r in rows
        if r['attempts'] >= min_attempts and r['efficiency'] is not None and _has_lesson(r.get('lesson'))
    ]
    filtered.sort(
        key=lambda x: (x['efficiency'], -x['attempts']),
        reverse=not hardest,
    )
    return filtered


def stuck_words(conn, source, today=None):
    today = today or date.today()
    rows = build_num_aggregates(conn, source, today, dict_only=True)
    out = []
    for r in rows:
        if not _has_lesson(r.get('lesson')):
            continue
        reasons = []
        if r['hard']:
            reasons.append('hard')
        if r['session_wrong']:
            reasons.append('session error')
        if r['attempts'] >= 3 and r['efficiency'] is not None and r['efficiency'] < 0.5:
            reasons.append('low efficiency')
        if not reasons:
            continue
        out.append({**r, 'reasons': ', '.join(reasons)})
    out.sort(key=lambda x: (-x['total_wrong'], x['efficiency'] if x['efficiency'] is not None else 2))
    return out


def srs_due_words(conn, source, today=None):
    today = today or date.today()
    rows = build_num_aggregates(conn, source, today, dict_only=True)
    due_rows = [r for r in rows if r['due'] and _has_lesson(r.get('lesson'))]
    due_rows.sort(
        key=lambda x: (
            0 if x['hard'] else 1,
            -(x['total_wrong']),
            x['days_since'] if x['days_since'] is not None else 9999,
        ),
    )
    return due_rows


def direction_asymmetry(conn, source, min_attempts=MIN_ATTEMPTS_DEFAULT, today=None):
    today = today or date.today()
    rows = build_num_aggregates(conn, source, today, dict_only=True)
    out = []
    for r in rows:
        if not _has_lesson(r.get('lesson')):
            continue
        dir_effs = []
        for direction, stat in r['directions'].items():
            ra, wa = stat.get('right_all', 0), stat.get('wrong_all', 0)
            if int(ra or 0) + int(wa or 0) < min_attempts:
                continue
            eff = efficiency(ra, wa)
            if eff is not None:
                dir_effs.append((direction, eff))
        if len(dir_effs) < 2:
            continue
        effs = [e for _, e in dir_effs]
        spread = max(effs) - min(effs)
        worst = min(dir_effs, key=lambda x: x[1])
        best = max(dir_effs, key=lambda x: x[1])
        out.append({
            **r,
            'spread': spread,
            'worst_dir': worst[0],
            'worst_eff': worst[1],
            'best_dir': best[0],
            'best_eff': best[1],
            'dir_detail': '; '.join(f'{d}: {format_pct(e)}' for d, e in sorted(dir_effs, key=lambda x: x[1])),
        })
    out.sort(key=lambda x: -x['spread'])
    return out


def get_unique_kanji_count(db_path=None):
    conn = open_db(db_path)
    try:
        cur = conn.execute(
            'SELECT DISTINCT "Kanji" FROM "Kanji" '
            "WHERE \"Kanji\" IS NOT NULL AND TRIM(\"Kanji\") != '' "
            "AND \"Kanji\" != 0 AND TRIM(CAST(\"Kanji\" AS TEXT)) NOT IN ('0', '0.0')"
        )
        return len(cur.fetchall())
    finally:
        conn.close()


def get_words_without_kanji_count(db_path=None):
    conn = open_db(db_path)
    try:
        return conn.execute('SELECT COUNT(*) FROM Kana').fetchone()[0]
    except sqlite3.OperationalError:
        return 0
    finally:
        conn.close()
