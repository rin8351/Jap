# -*- coding: utf-8 -*-
"""Reset Jp.db to a small English demo dataset for portfolio use."""
import os
import random
import sqlite3
from datetime import date, timedelta

from stats_script import ensure_all_stats_tables, iter_stats_table_names, STATS_SOURCES

DB_PATH = os.path.join(os.path.dirname(__file__), 'Jp.db')
TODAY = date.today()

KANJI_ROWS = [
    (1, 1, '日', 'ニチ、ジツ', 'ひ、-び', 'day, sun', 'Noun', ''),
    (2, 1, '人', 'ジン、ニン', 'ひと', 'person', 'Noun', ''),
    (3, 1, '本', 'ホン', 'ほん、もと', 'book', 'Noun', ''),
    (4, 1, '火', 'カ', 'ひ、-び', 'fire', 'Noun', ''),
    (5, 1, '学', 'ガク', 'まな.ぶ', 'study, learning', 'Noun', ''),
]

WORDS_ROWS = [
    (1, 1, '火山', 'かざん', 'volcano', ''),
    (2, 1, '日本', 'にほん', 'Japan', ''),
    (3, 1, '大学', 'だいがく', 'university', ''),
]

FRAZES_ROWS = [
    (1, 1, 'きいてください', 'きいてください', 'Please listen'),
    (2, 1, 'はじめまして', 'はじめまして', 'Nice to meet you'),
    (3, 1, 'いいえ、ちがいます', 'いいえ、ちがいます', "No, that's not correct"),
    (4, 1, '日本語ではなしてください', 'にほんごではなしてください', 'Please speak in Japanese'),
    (5, 1, 'もう一度、どうぞ', 'もういちど、どうぞ', 'Once more, please'),
]

KANA_ROWS = [
    (1, 1, 'どうぞ', 'please / go ahead', 'Adverb', ''),
    (2, 1, 'ねこ', 'cat', 'Noun', ''),
    (3, 1, 'つぎ', 'next', 'Adverb', ''),
    (4, 1, 'いい', 'good', 'Adjective', ''),
    (5, 1, 'すぐ', 'immediately', 'Adverb', ''),
    (6, 1, 'また', 'again', 'Adverb', ''),
]

NAME_ROWS = [
    (1, 1, '田中', 'たなか'),
    (2, 1, '山田', 'やまだ'),
    (3, 1, '佐藤', 'さとう'),
]

STAT_PROFILES = [
    # Untested — leave as inserted by ensure_all_stats_tables
    None,
    # Due for review (normal)
    {
        'difficulty': 'normal', 'wrong': 0, 'right': 2,
        'last_right': (TODAY - timedelta(days=5)).strftime('%d.%m.%Y'),
        'interval_days': 2, 'right_all': 8, 'wrong_all': 2,
    },
    # Hard / stuck
    {
        'difficulty': 'hard', 'wrong': 2, 'right': 0,
        'last_right': (TODAY - timedelta(days=1)).strftime('%d.%m.%Y'),
        'interval_days': 1, 'right_all': 4, 'wrong_all': 12,
    },
    # Easy / mastered
    {
        'difficulty': 'easy', 'wrong': 0, 'right': 5,
        'last_right': (TODAY - timedelta(days=30)).strftime('%d.%m.%Y'),
        'interval_days': 30, 'right_all': 25, 'wrong_all': 1,
    },
    # Low accuracy
    {
        'difficulty': 'normal', 'wrong': 1, 'right': 0,
        'last_right': (TODAY - timedelta(days=3)).strftime('%d.%m.%Y'),
        'interval_days': 2, 'right_all': 3, 'wrong_all': 9,
    },
    # Recently correct, not due yet
    {
        'difficulty': 'normal', 'wrong': 0, 'right': 1,
        'last_right': TODAY.strftime('%d.%m.%Y'),
        'interval_days': 4, 'right_all': 6, 'wrong_all': 0,
    },
]


def _clear_all(conn):
    tables = [
        r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        ).fetchall()
    ]
    conn.execute('PRAGMA foreign_keys=OFF')
    for name in tables:
        conn.execute(f'DELETE FROM "{name}"')


def _insert_dict_data(conn):
    conn.executemany(
        'INSERT INTO "Kanji" (Num, Lesson, Kanji, "On", Kun, Trans, Sush, Mnem) VALUES (?,?,?,?,?,?,?,?)',
        KANJI_ROWS,
    )
    conn.executemany(
        'INSERT INTO "Words" (Num, Lesson, Kanji, Read, Trans, Mnem) VALUES (?,?,?,?,?,?)',
        WORDS_ROWS,
    )
    conn.executemany(
        'INSERT INTO "Frazes" (Num, Lesson, Kanji, Read, Trans) VALUES (?,?,?,?,?)',
        FRAZES_ROWS,
    )
    conn.executemany(
        'INSERT INTO "Kana" (Num, Lesson, Kun, Trans, Sush, Mnem) VALUES (?,?,?,?,?,?)',
        KANA_ROWS,
    )
    conn.executemany(
        'INSERT INTO "Name" (Num, Lesson, Kanji, Read) VALUES (?,?,?,?)',
        NAME_ROWS,
    )


def _fmt_date(d):
    return d.strftime('%d.%m.%Y')


def _seed_stats(conn):
    rng = random.Random(42)
    update_sql = (
        'UPDATE "{table}" SET difficulty=?, wrong=?, "right"=?, last_right=?, '
        'interval_days=?, right_all=?, wrong_all=? '
        'WHERE num=? AND value=? AND answer=?'
    )
    for source, (prefix, columns) in STATS_SOURCES.items():
        for table_name in iter_stats_table_names(prefix, columns):
            rows = conn.execute(
                f'SELECT num, value, answer FROM "{table_name}"'
            ).fetchall()
            for num, value, answer in rows:
                profile = rng.choice(STAT_PROFILES)
                if profile is None:
                    continue
                conn.execute(
                    update_sql.format(table=table_name),
                    (
                        profile['difficulty'],
                        profile['wrong'],
                        profile['right'],
                        profile['last_right'],
                        profile['interval_days'],
                        profile['right_all'],
                        profile['wrong_all'],
                        num,
                        value,
                        answer,
                    ),
                )


def main():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    try:
        _clear_all(conn)
        _insert_dict_data(conn)
        conn.commit()
        ensure_all_stats_tables(conn)
        _seed_stats(conn)
        conn.commit()
        conn.execute('PRAGMA wal_checkpoint(TRUNCATE)')
        conn.execute('PRAGMA journal_mode=DELETE')
        conn.execute('VACUUM')
    finally:
        conn.close()

    for extra in ('Jp.db-wal', 'Jp.db-shm'):
        if os.path.exists(os.path.join(os.path.dirname(DB_PATH), extra)):
            os.remove(os.path.join(os.path.dirname(DB_PATH), extra))

    size_kb = os.path.getsize(DB_PATH) // 1024
    print(f'Demo database ready ({size_kb} KB)')
    conn = sqlite3.connect(DB_PATH)
    for table in ('Kanji', 'Words', 'Frazes', 'Kana', 'Name'):
        n = conn.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
        print(f'  {table}: {n} rows')
    stat_tables = [
        r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        ).fetchall()
        if r[0][0].islower()
    ]
    total_stat_rows = sum(
        conn.execute(f'SELECT COUNT(*) FROM "{name}"').fetchone()[0]
        for name in stat_tables
    )
    active = conn.execute(
        'SELECT COUNT(*) FROM kanji_trans_kanji WHERE right_all > 0 OR wrong_all > 0'
    ).fetchone()[0]
    print(f'  stats: {total_stat_rows} rows across {len(stat_tables)} tables ({active} with history in kanji_trans_kanji)')
    conn.close()


if __name__ == '__main__':
    main()
